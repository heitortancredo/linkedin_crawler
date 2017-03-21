Requisitos:
    - phamtonJS Webdriver
    - Selenium
    - Scrapy

OBS.: Eh necessario adicionar ao PYTHONPATH o path de onde encontra-se o projeto.

Ex.:

    $ echo $PYTHONPATH 
    $ /Users/heitortancredo/Documents/Intexfy/selenium_linkedin/linkedin_selenium_crawler



Uso:
    
    classes:
        CompanyCrawler(login, senha)
        PersonCrawler(login, senha)
            * login: string correspondente ao usuario no linkedin
            * senha: string correspondente a senha respectiva do usuario no linkedin 

            Ex,:
                crwl = PersonCrawler("teste@teste.com", "Teste1234")
                crwl = CompanyCrawler("teste@teste.com", "Teste1234")

    funcoes disponíveis:
        - run_crawler(perfil):
            * perfil: é a string correspondente ao perfil que deseja-se 'crawlear'
                Ex.: crwl.run_crawler('in/heitortancredo')
                     crwl.run_crawler('15259438')


    Exemplo:

            from intexfy_company_crawler import CompanyCrawler
            import pprint

            def main():
                crwl = CompanyCrawler("teste@teste.com", "Teste1234")
                r = crwl.run_crawler("15259438")
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(r)

            if __name__ == "__main__":
                main()


Estrutura de retorno:


PERSON
-------

[ { 'following': { 'companies': [ u'Startup Weekend',
                                  u'WEG',
                                  u'Funda\xe7\xe3o Getulio Vargas',
                                  u'TED: Ideas Worth Spreading - Unofficial',
                                  u'Web Summit',
                                  u'UP Global'],
                   'peoples': [ u'Tiffany Bass Bukow',
                                u'Brad Feld',
                                u'Marvin Scaff',
                                u'Cody Simms',
                                u'Vanesa Kolodziej',
                                u'In Hsieh',
                                u'Karen Mooney',
                                u'Dave Parker',
                                u'Vinicius Miana',
                                u'Felipe Matos']},
    'infos': { 'address_summary': u'S\xe3o Paulo, S\xe3o Paulo, Brasil',
               'dateofbirth': u'6 de janeiro',
               'email': [u'andrehotta@gmail.com'],
               'foto': u'https://media.licdn.com/mpr/mpr/shrinknp_400_400/p/8/005/057/147/05ef412.jpg',
               'full_name': u'Andr\xe9 Hotta',
               'in_empresa': u'https://www.linkedin.com/company-beta/15259438/',
               'perfil_in': u'linkedin.com/in/andrehotta',
               'phone': [u'+55 11964076009 (Celular)'],
               'position_company_name': u'Intexfy',
               'position_title': u'Co-founder at Intexfy',
               'site': [u'http://techstars.com/', u'http://intexfy.com/'],
               'social_twitter_handle': u'https://twitter.com/andrehotta'},
    'language_name': [ u'Idioma\nAlem\xe3o\nN\xedvel b\xe1sico',
                       u'Idioma\nIngl\xeas\nN\xedvel avan\xe7ado',
                       u'Idioma\nPortugu\xeas\nFluente ou nativo'],
    'skill_name': [ u'Entrepreneurship',
                    u'Business Strategy',
                    u'Start-ups',
                    u'Start-up Environment',
                    u'Community Management',
                    u'Business Planning',
                    u'Coworking',
                    u'Lean Startup',
                    u'Event Planning',
                    u'Startup Development',
                    u'New Business Development',
                    u'Community Building',
                    u'Community Development',
                    u'Process Engineering',
                    u'Business Analysis',
                    u'Event Management',
                    u'Product Development',
                    u'Collaboration',
                    u'Lean Manufacturing',
                    u'Logical Thinker',
                    u'Business Modeling',
                    u'Team Leadership',
                    u'Project Management',
                    u'Marketing Strategy',
                    u'Strategic Planning',
                    u'Leadership',
                    u'Digital Marketing',
                    u'Management',
                    u'Negotiation',
                    u'Strategy',
                    u'Business Development']}]

COMPANY
--------

[   {   'address_city': u'Florian\xf3polis, Santa Catarina',
        'category_industry': u'Tecnologia da informa\xe7\xe3o e servi\xe7os',
        'company_employees': {   u'Andr\xe9 Hotta': [   u'https://www.linkedin.com/in/andrehotta/',
                                                        u'Co-founder at Intexfy'],
                                 u'Eduardo Mattos': [   u'https://www.linkedin.com/in/edusmattos/',
                                                        u'--'],
                                 u'Wesley Lino': [   u'https://www.linkedin.com/in/wesley-linoo/',
                                                     u'Inside Sales Representative na Intexfy']},
        'description': u'A Intexfy automatiza a an\xe1lise de dados para aumentar a prospec\xe7\xe3o de vendas. Por meio de Intelig\xeancia artificial, Machine Learning e Marketing Preditivo a Intexfy  identifica, qualifica e gera os melhores prospects e leads.',
        'employees': u'2-10 funcion\xe1rios',
        'logo': u'https://media.licdn.com/mpr/mpr/shrink_200_200/AAEAAQAAAAAAAAgnAAAAJDk1MmNjNjAxLWJlNWItNDJjNy1hMTNkLWExMWQzMWY1Y2UzZQ.png',
        'name': u'Intexfy',
        'relates': {   u'AFSKINS.com': [   u'https://www.linkedin.com/company-beta/15264421/',
                                           u'2-10 funcion\xe1rios',
                                           u'Materiais esportivos'],
                       u'Alpha Ledger': [   u'https://www.linkedin.com/company-beta/15265178/',
                                            u'2-10 funcion\xe1rios',
                                            u'Gest\xe3o de investimentos'],
                       u'Ecentiva': [   u'https://www.linkedin.com/company-beta/2943505/',
                                        u'2-10 funcion\xe1rios',
                                        u'Tecnologia da informa\xe7\xe3o e servi\xe7os'],
                       u'SEPROL LIMITED': [   u'https://www.linkedin.com/company-beta/5720313/',
                                              u'11-50 funcion\xe1rios',
                                              u'Tecnologia da informa\xe7\xe3o e servi\xe7os'],
                       u'Santler Digital': [   u'https://www.linkedin.com/company-beta/10653346/',
                                               u'2-10 funcion\xe1rios',
                                               u'Design'],
                       u'Techstars': [   u'https://www.linkedin.com/company-beta/167750/',
                                         u'51-200 funcion\xe1rios',
                                         u'Capital de risco e participa\xe7\xf5es privadas']},
        'specialities': u'sales, marketing, business intelligence, artificial intelligence, vendas, predictable sales, predictable revenue, machine learning, prospect e prospec\xe7ao',
        'start': u'2016',
        'url': u'http://www.intexfy.com/'}]
