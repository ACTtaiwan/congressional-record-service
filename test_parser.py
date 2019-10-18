from handler import scrape

data = scrape()
file_name = f"{data['date']}"
print(data)
print(file_name)