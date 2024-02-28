import pyjokes
import wikipedia
import requests
from colorama import Fore
import webbrowser

def Bot(query):
    query = query[5:]
    if query == "BES":
        print(Fore.GREEN + "𓀳 This is BES - GOD OF HUMOUR\nI shall humor you with my finest ones!!\n")
        loop = True
        while loop:
            My_joke = pyjokes.get_joke(language="en", category="all")
            print(Fore.YELLOW + " 📢 " + My_joke)
            print("\n")
            dec = input(Fore.BLUE + "Want any more(Y/N): ")
            if dec == 'N':
                loop = False
        print(Fore.WHITE + "\n")
    elif query == "THOTH":
        print(Fore.GREEN + "𓁵 This is THOTH - GOD OF WISDOM\nI shall grace you with some info \n")
        info = input("What do you want to know about: ")
        search_result_keys = wikipedia.search(info, results=7)
        print("Search Results are:")
        for i in search_result_keys:
            print(" 🏷️ " + i)
        print("\n")
        info_after_search = input("Enter the search keyword: ")
        result = wikipedia.summary(info_after_search, sentences=3)
        print(Fore.YELLOW + result)
        print(Fore.WHITE + "\n")
    elif query == "ANUBIS":
        print(Fore.GREEN + "𓁢 This is ANUBIS - GOD OF THE AFTERLIFE\nI begin the REPORT.....")
        def NewsFromBBC():
            query_params = {
                "source": "bbc-news",
                "sortBy": "top",
                "apiKey": "17c0b2ffa88247c895fd907e78d20510"
            }
            main_url = " https://newsapi.org/v1/articles"
        
            res = requests.get(main_url, params=query_params)
            open_bbc_page = res.json()
        
            article = open_bbc_page["articles"]
        
            results = []
            
            for ar in article:
                results.append(ar["title"])
                
            for i in range(len(results)):
                print(Fore.YELLOW + " 📰 ", results[i])
        NewsFromBBC()
        print(Fore.WHITE + "\n")
    elif query == "RA":
        loop_choice = True
        while loop_choice:
            print(Fore.GREEN + "𓁴 This is RA - THE SUN GOD\nSAYETH THY WISH.....")
            print(Fore.YELLOW + " 𓂀  1 - Open Youtube\n 𓃕  2 - Open Google\n 𓄎  3 - Open PesuAcademy\n 𓅄  4 - Open NETFLIX\n")
            choice = input('')
            if choice == '1':
                webbrowser.open('https://www.youtube.com/')
                loop_choice = False
            elif choice == '2':
                webbrowser.open('https://www.google.com/')
                loop_choice = False
            elif choice == '3':
                webbrowser.open('https://www.pesuacademy.com/Academy/')
                loop_choice = False
            elif choice == '4':
                webbrowser.open('https://www.netflix.com/in/')
                loop_choice = False
            else:
                print("YOU CHOSE WRONG!!\nHa!! Ha!! CHOOSE AGAIN\n")
        print(Fore.WHITE + "\n")
    elif query == "ALL":
        print(Fore.BLUE + " 𓌅 BES - GOD OF HUMOUR\n 𓌍 THOTH - GOD OF WISDOM\n 𓎞 ANUBIS - GOD OF THE AFTERLIFE\n 𓎬 RA - THE SUN GOD")
    else:
        print(Fore.RED + "That GOD is either not available, OR YOU SPELT HIM WRONG!! \nMAY YOU PERISH WITH SANDS OF ANUBIS!!!")