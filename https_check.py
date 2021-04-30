import requests
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--headers", help="print the http headers of the http response", action="store_true")
    parser.add_argument("-b", "--body", help="print the body of the http response", action="store_true")
    parser.add_argument("-r", "--results", help="print the url and status code of the successful http response", action="store_true")
    parser.add_argument("-s", "--save", help="Save the body to a file", action="store_true")
    parser.add_argument("-f", "--file", help="Specify input file with a list of hostnames to be checked", action="store")
    return parser.parse_args()

def request_https(host):
    r=requests.get("https://" + host.strip())
    return r

def request_http(host):
    r=requests.get("http://" + host.strip())
    return r

def print_hresponse(h):
    print(f"HTTP request for URL: {h.url} RESULT: {h.status_code}")
    for response in h.history:
        print("Historical HTTP url: " + str(response.url))
        print("Historical HTTP response code: " + str(response.status_code))

def print_response(args,r):
    print(f"HTTPS request for URL: {r.url} RESULT: {r.status_code}")
    for response in r.history:
        print("Historical HTTPS url: " + str(response.url))
        print("Historical HTTPS response code: " + str(response.status_code))  
    if args.headers:
        print ("\n========= HEADERS ==========\n", r.headers)
    if args.body and args.save:
        output = open("http_output.txt",'w')
        output.write(r.text)
        output.close()
    elif args.body:
        print ("============ BODY =============\n", r.text)

def main():
    args=parse_args()
    if not args.file:
        print("A file containing a list of domains is required for script input")
        quit()
    with open(args.file,"r") as file:
        hosts = file.readlines() 
        for host in hosts:
            try:
                h=request_http(host)
                if args.results:
                    print ("\n========= RESULTS ==========")
                    print_hresponse(h)
                if not "https" in h.url:
                    print(f"**** {h.url} is an HTTP SITE!!! ****\n")
            except requests.exceptions.RequestException as e:
                print("**** EXCEPTION WITH HOST: " + host)
                print(str(e)+"\n")
            try:
                r=request_https(host)
                if args.results:
                    print_response(args,r)
            except requests.exceptions.RequestException as e:
                print("**** EXCEPTION WITH HOST: " + host.strip() + "****\n")
                print(str(e)+"\n")

if __name__ == "__main__":
    main()
