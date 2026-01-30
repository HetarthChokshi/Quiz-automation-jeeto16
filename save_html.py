import requests

def download_html(url, output_file="website-page-5.html"):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes

        with open(output_file, "w", encoding=response.encoding or "utf-8") as file:
            file.write(response.text)

        print(f"HTML successfully downloaded and saved as '{output_file}'")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the website: {e}")

if __name__ == "__main__":
    # website_url = "https://jeeto16cr.com/auth/register?qr=1768044780917_3&language=g&mode=online&groupType=db" #1
    # website_url = "https://jeeto16cr.com/auth/login?qr=1768044780917_3&language=g&mode=online&groupType=db" #2
    # website_url = "https://jeeto16cr.com/user/scan-progress" #3
    # website_url = "https://jeeto16cr.com/select-language" #0
    website_url = "https://jeeto16cr.com/homes" #5
    
    download_html(website_url)
