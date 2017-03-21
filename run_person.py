from intexfy_person_crawler import PersonCrawler
import pprint

login = ""
password = ""
perfil = ""


def main():
    crwl = PersonCrawler(login, password)
    r = crwl.run_crawler(perfil)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(r)

if __name__ == "__main__":
    main()
