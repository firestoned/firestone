// This file is NOT auto-generated - manually created to combine CLI and server functionality
// Similar to examples/addressbook/main.py in Python

use clap::{Parser, Subcommand};
use std::sync::Arc;
use tokio::net::TcpListener;

// Auto-generated modules (from openapi-generator)
pub mod apis;
pub mod models;

// Auto-generated CLI modules (from firestone)
mod cli;

// Manually created modules
mod server;

use apis::configuration::Configuration;

#[derive(Parser, Debug)]
#[command(name = "addressbook_rs")]
#[command(version = "1.0.0")]
#[command(about = "Addressbook CLI and Server", long_about = "This is the CLI and server for the example Addressbook")]
struct Cli {
    /// Turn on debugging
    #[arg(long)]
    debug: bool,

    /// The API key to authorize against API
    #[arg(long)]
    api_key: Option<String>,

    /// The API url, e.g. http://localhost:8080
    #[arg(long)]
    api_url: Option<String>,

    /// Run the server instead of CLI
    #[arg(long)]
    server: bool,

    /// Server port (default: 8080)
    #[arg(long, default_value = "8080")]
    port: u16,

    /// Server host (default: 0.0.0.0)
    #[arg(long, default_value = "0.0.0.0")]
    host: String,

    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Addressbook operations
    #[command(subcommand)]
    Addressbook(cli::addressbook::AddressbookCommands),
    /// Person operations
    #[command(subcommand)]
    Persons(cli::persons::PersonsCommands),
    /// Postal code operations
    #[command(subcommand)]
    PostalCodes(cli::postal_codes::PostalCodesCommands),
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();

    // Initialize logging
    let log_level = if cli.debug {
        log::LevelFilter::Debug
    } else {
        log::LevelFilter::Info
    };
    env_logger::Builder::from_default_env()
        .filter_level(log_level)
        .init();

    // If --server flag is set, run the server
    if cli.server {
        return run_server(&cli.host, cli.port).await;
    }

    // Otherwise, run CLI commands
    let api_url = cli.api_url.unwrap_or_else(|| "http://localhost:8080".to_string());
    let mut config = Configuration::default();
    config.base_path = api_url.clone();
    if let Some(api_key) = cli.api_key {
        // Set API key in configuration if needed
        // config.api_key = Some(apis::ApiKey { prefix: Some("Bearer".to_string()), key: api_key });
    }

    // openapi-generator Rust client uses standalone functions, not API structs
    // So we just pass the Configuration to the CLI handlers
    let config_arc = Arc::new(config);

    match cli.command {
        Some(Commands::Addressbook(cmd)) => {
            let ctx = cli::addressbook::ApiContext {
                api_client: config_arc.clone(),
            };
            cli::addressbook::handle_addressbook_command(&ctx, &cmd).await?;
        }
        Some(Commands::Persons(cmd)) => {
            let ctx = cli::persons::ApiContext {
                api_client: config_arc.clone(),
            };
            cli::persons::handle_persons_command(&ctx, &cmd).await?;
        }
        Some(Commands::PostalCodes(cmd)) => {
            let ctx = cli::postal_codes::ApiContext {
                api_client: config_arc.clone(),
            };
            cli::postal_codes::handle_postal_codes_command(&ctx, &cmd).await?;
        }
        None => {
            eprintln!("No command specified. Use --help for usage information.");
            eprintln!("Use --server to run the server.");
            std::process::exit(1);
        }
    }

    Ok(())
}

async fn run_server(host: &str, port: u16) -> Result<(), Box<dyn std::error::Error>> {
    let app = server::create_router();
    let addr = format!("{}:{}", host, port);
    let listener = TcpListener::bind(&addr).await?;
    
    println!("Server running on http://{}", addr);
    println!("API documentation available at http://{}/openapi.json", addr);
    
    axum::serve(listener, app).await?;
    Ok(())
}

