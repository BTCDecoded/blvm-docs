use std::io;
use std::process;

use clap::{Arg, Command};
use mdbook::errors::Error;
use mdbook::preprocess::{CmdPreprocessor, Preprocessor};
use mdbook_governance_vars::GovVarsPreprocessor;
use semver::{Version, VersionReq};

pub fn make_app() -> Command {
    Command::new("mdbook-governance-vars")
        .about("Expand [[gov:KEY]] from governance YAML for blvm-docs")
        .subcommand(
            Command::new("supports").arg(
                Arg::new("renderer")
                    .required(true)
                    .help("Renderer to support (e.g. html)"),
            ),
        )
}

fn main() {
    let matches = make_app().get_matches();
    let preprocessor = GovVarsPreprocessor;

    if let Some(sub_args) = matches.subcommand_matches("supports") {
        handle_supports(&preprocessor, sub_args);
    } else if let Err(e) = handle_preprocessing(&preprocessor) {
        eprintln!("{e}");
        process::exit(1);
    }
}

fn handle_preprocessing(pre: &dyn Preprocessor) -> Result<(), Error> {
    let (ctx, book) = CmdPreprocessor::parse_input(io::stdin())?;

    let book_version = Version::parse(&ctx.mdbook_version)?;
    let version_req = VersionReq::parse(mdbook::MDBOOK_VERSION)?;
    if !version_req.matches(&book_version) {
        eprintln!(
            "Warning: {} was built against mdbook {}, called from {}",
            pre.name(),
            mdbook::MDBOOK_VERSION,
            ctx.mdbook_version
        );
    }

    let processed_book = pre.run(&ctx, book)?;
    serde_json::to_writer(io::stdout(), &processed_book)?;
    Ok(())
}

fn handle_supports(pre: &dyn Preprocessor, sub_args: &clap::ArgMatches) -> ! {
    let renderer = sub_args
        .get_one::<String>("renderer")
        .expect("renderer required");
    if pre.supports_renderer(renderer) {
        process::exit(0);
    }
    process::exit(1);
}
