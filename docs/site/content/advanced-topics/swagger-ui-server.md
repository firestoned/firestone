---
title: "Using the Integrated Swagger UI Server"
weight: 3
---

# Operations: Using the Integrated Swagger UI Server

One of Firestone's most powerful features for development and debugging is its ability to serve your generated OpenAPI specification with a live, interactive Swagger UI documentation site. This allows you to visualize and interact with your API endpoints without writing any client code.

## What is Swagger UI?

Swagger UI is a tool that takes an OpenAPI specification and generates a beautiful, interactive API documentation website. It allows developers and testers to:

-   See all available API endpoints, methods, and parameters.
-   Read descriptions for each operation and data model.
-   Try out API calls directly from the browser.
-   View example request and response payloads.
-   Authenticate and make authorized API calls.

## How to Start the UI Server

Firestone makes this incredibly easy with the `--ui-server` flag for the `generate openapi` command.

1.  **Run the Command**: Navigate to your project directory and run the following command, pointing to your resource schema(s):

    ```bash
    firestone generate \
        --title "My API" \
        --resources ./resources/ \
        openapi \
        --ui-server
    ```

2.  **Access the UI**: Firestone will start a local web server. By default, you can access the Swagger UI in your browser at:

    **http://127.0.0.1:8000**

    The server will also automatically open your default web browser to this address.

3.  **Live Reload**: The UI server watches your resource schema files for changes. If you save a change to any of your resource files, Firestone will automatically regenerate the OpenAPI specification and reload the Swagger UI page in your browser. This provides an instant feedback loop for API design.

## Interacting with Your API

Once the Swagger UI is running, you can explore and test your API.

-   **Endpoints**: Each API path (e.g., `/users` and `/users/{user_id}`) is listed. Click on an endpoint to expand its available methods.
-   **"Try it out"**: For any operation, click the "Try it out" button. This will make the parameter fields editable.
-   **Parameters**: Fill in any required parameters, such as an ID for a `GET /users/{user_id}` request or a JSON body for a `POST /users` request.
-   **Execute**: Click the "Execute" button to make a live API call.

**Note**: The "Execute" button makes a real HTTP request from your browser to the server URL defined in the OpenAPI specification (by default, `/`). This will likely result in a "network error" because your actual backend API is not running at that address. The UI server's purpose is to *visualize* the API contract; it does not mock the API's implementation. To handle the requests, you would need to run a separate backend server (like one generated with `firestone generate server`) that implements the API.

## Authenticating in Swagger UI

If you have defined security schemes in your resource schema, an "Authorize" button will appear at the top right of the Swagger UI page.

1.  **Click "Authorize"**: A dialog box will appear with fields for each security scheme you've defined.
2.  **Enter Credentials**: For a `bearerAuth` scheme, you would paste your JWT into the value field. For an `apiKeyAuth`, you would enter your API key.
3.  **Authorize**: Click the "Authorize" button in the dialog.

Once authorized, every request you make by clicking "Execute" will automatically include the necessary `Authorization` header or API key. This is an excellent way to test protected endpoints.
