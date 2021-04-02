import os, sys, csv, requests, time
from tqdm import tqdm
from pprint import pprint


class NotFoundChecker():

    def __init__(self):

        self.start_on = 0
        self.column = 0

        self.links = []

    def write_csv_file_of_request_codes(self, linklist):

        with open("request_codes.csv", 'w', newline="") as f:

            csv_writer = csv.writer(f)
            csv_writer.writerow(["Link", "Status Code"])

            for l in tqdm(linklist):

                link_status_code = self.get_link_status_code(l)

                csv_writer.writerow([l, link_status_code])
                time.sleep(0.3)

    def get_links_that_return_not_found(self, linklist):

        not_found_links = []

        for l in tqdm(linklist[self.start_on:]):
            if self.returns_server_not_found(l):
                not_found_links.append(l)

        return not_found_links

    def get_link_list_from_file(self, file):

        with open(file, 'r') as f:

            csv_reader = csv.reader(f)
            csv_lines = [row for row in csv_reader][self.start_on:]

        return [row[self.column] for row in csv_lines]

    def get_link_status_code(self, link):

        #todo check for http connections

        if link[:4] == "https":
            https_link = link
        else:
            https_link = "https://" + link

        return requests.get(https_link).status_code

    def is_valid_with_protocol(self, link, protocol):
        http_link = protocol + "://" + link
        r = requests.get(http_link)

        return False if r.status_code == 404 else True

    def get_valid_url(self, link):
        if link[:3] == "http":
            return link

nfc = NotFoundChecker()
nfc.start_on = 1
nfc.column = 1

nfc.links = nfc.get_link_list_from_file("gh-redirects.csv")
nfc.write_csv_file_of_request_codes(nfc.links)