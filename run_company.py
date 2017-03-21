from intexfy_company_crawler import CompanyCrawler
import pprint

login = ""
password = ""
perfil = ""

def main():
    crwl = CompanyCrawler(login, password)
    r = crwl.run_crawler(perfil)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(r)

if __name__ == "__main__":
    main()
