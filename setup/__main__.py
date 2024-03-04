def main():
  from setup.tray import tray
  from setup.app_setup import app_setup

  app_setup()
  tray.run()


if __name__ == "__main__":
  main()
