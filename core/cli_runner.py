import argparse
def run():
    parser = argparse.ArgumentParser(description="Run Elytrix strategy engine.")
    parser.add_argument("--mode", type=str, required=True)
    parser.add_argument("--strategy", type=str, required=True)
    parser.add_argument("--config", type=str, default="config/test_config.json")
    args = parser.parse_args()
    print(f"Running in mode={args.mode} with strategy={args.strategy}")
if __name__ == "__main__":
    run()
