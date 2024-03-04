# ruff: noqa: F401

if __name__ == "__main__":
  from server.app import app
  import server.common_routes
  import server.entrypoint_routes
  import server.video_routes
  import server.character_routes

  app.run()
