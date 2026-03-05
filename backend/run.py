import uvicorn

BANNER = r"""
  _____ ____  _____ _   _ ____       _    ____ _____ _   _ _____
 |_   _|  _ \| ____| \ | |  _ \     / \  / ___| ____| \ | |_   _|
   | | | |_) |  _| |  \| | | | |   / _ \| |  _|  _| |  \| | | |
   | | |  _ <| |___| |\  | |_| |  / ___ \ |_| | |___| |\  | | |
   |_| |_| \_\_____|_| \_|____/  /_/   \_\____|_____|_| \_| |_|

  AI Web Monitoring & Trend Detection Agent v1.0
  Backend: http://localhost:8000
  API Docs: http://localhost:8000/docs
"""

if __name__ == "__main__":
    print(BANNER)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
