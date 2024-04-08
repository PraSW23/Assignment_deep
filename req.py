import requests

class HTMLParser:
    def __init__(self, html_content):
        self.html_content = html_content
        self.position = 0

    def find_next_tag(self, tag_name):
        start_tag = f"<{tag_name}"
        end_tag = f"</{tag_name}>"

        start_tag_index = self.html_content.find(start_tag, self.position)
        if start_tag_index == -1:
            return None, None  

        end_tag_index = self.html_content.find(end_tag, start_tag_index)
        if end_tag_index == -1:
            return None, None  

        tag_content = self.html_content[start_tag_index:end_tag_index + len(end_tag)]
        self.position = end_tag_index + len(end_tag)
        return tag_content, end_tag_index + len(end_tag)

    def parse(self):
        stories_data = []

        while True:
            li_tag, end_index = self.find_next_tag("li")
            if not li_tag:
                break
            
            # Checking if the <li> tag has the class 'latest-stories__item'
            if 'latest-stories__item' not in li_tag:
                continue

            title_tag, _ = self.find_next_tag("h3")
            if title_tag is None:
                print("Error: Title tag not found")
                print("HTML Content:", li_tag)
                continue

            title_start_index = title_tag.find(">") + 1
            title_end_index = title_tag.find("</h3>")
            title = title_tag[title_start_index:title_end_index].strip()

            link_tag, _ = self.find_next_tag("a")
            if link_tag is None:
                print("Error: Link tag not found")
                print("HTML Content:", li_tag)
                continue

            link_start_index = link_tag.find("href=\"") + len("href=\"")
            link_end_index = link_tag.find("\"", link_start_index)
            link = link_tag[link_start_index:link_end_index]
            full_link = f"https://time.com{link}"
            stories_data.append({"title": title, "link": full_link})
            self.position = end_index

        return stories_data

def get_time_stories():
    # Sending a GET request to the Time.com website
    response = requests.get("https://time.com")

    
    if response.status_code == 200:
        parser = HTMLParser(response.text)
        return parser.parse()
    else:
        return []


if __name__ == "__main__":
    time_stories = get_time_stories()
    print(time_stories)
