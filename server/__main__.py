if __name__ == "__main__":
    from server.app import app
    import server.common_routes
    import server.entrypoint_routes

    app.run()
