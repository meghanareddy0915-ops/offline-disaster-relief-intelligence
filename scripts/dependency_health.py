import importlib.metadata


def main():
    streamlit_version = importlib.metadata.version("streamlit")
    major = int(streamlit_version.split(".", maxsplit=1)[0])
    if major < 1:
        raise SystemExit(f"Unsupported Streamlit version: {streamlit_version}")

    print(f"dependency health passed: streamlit {streamlit_version}")


if __name__ == "__main__":
    main()
