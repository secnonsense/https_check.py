import requests
import argparse
import socket

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--headers", help="print the http headers of the http response", action="store_true")
    parser.add_argument("-b", "--body", help="print the body of the http response", action="store_true")
    parser.add_argument("-r", "--results", help="print the url and status code of the successful http response", action="store_true")
    parser.add_argument("-s", "--save", help="Save the body to a file", action="store_true")
    parser.add_argument("-o", "--output", help="Save the output of the command to a file", action="store_true")
    parser.add_argument("-f", "--file", help="Specify input file with a list of hostnames to be checked", action="store")
    return parser.parse_args()

def request_https(host):
    r=requests.get("https://" + host.strip(),timeout=4)
    return r

def request_http(host):
    r=requests.get("http://" + host.strip(),timeout=4)
    return r

def print_hresponse(h):
    print(f"HTTP request for URL: {h.url} RESULT: {h.status_code}")
    for response in h.history:
        print("Historical HTTP url: " + str(response.url))
        print("Historical HTTP response code: " + str(response.status_code))

def print_response(args,r):
    if not "https" in r.url:
                    print(f"**** {r.url} is an HTTP SITE!!! ****\n")
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

def file_response(r,output,x):
        if not "https" in r.url:
                    output.write(f"\n**** {r.url} is an HTTP SITE!!! ****\n")
        output.write(f"\n{x} request for URL: {r.url} RESULT: {r.status_code}\n")
        for response in r.history:
            output.write(f"Historical {x} url: {response.url}\n")
            output.write(f"Historical {x} response code: {response.status_code}\n")  


def main():
    args=parse_args()
    if not args.file:
        print("A file containing a list of domains is required for script input")
        quit()
    with open(args.file,"r") as file:
        hosts = file.readlines()
        with open("https_output.txt",'w') as output:
            for host in hosts:
                try:
                    h=request_http(host)
                    if args.results:
                        print ("\n========= RESULTS ==========")
                        print_hresponse(h)
                    if args.output:
                        output.write("\n========= RESULTS ==========")
                        output.write(f"\nIP address: {socket.gethostbyname(host.strip())}")
                        output.write(f"\nHostname: {host}")
                        file_response(h,output,x="HTTP")
                except requests.exceptions.RequestException as e:
                    print("\n**** EXCEPTION WITH HTTP HOST: " + host.strip() + " ****\n")
                    print(str(e)+"\n")
                    output.write("\n========= RESULTS ==========")
                    try:
                        output.write(f"\nIP address: {socket.gethostbyname(host.strip())}")
                    except socket.gaierror as j:
                        output.write(f'\nIP not resolved, error raised is {j}')
                    output.write(f"\nHostname: {host}")
                    output.write("\n**** EXCEPTION WITH HTTP HOST: " + host.strip() + " ****\n")
                    output.write(str(e)+"\n")
                try:
                    r=request_https(host)
                    if args.results:
                        print_response(args,r)
                    if args.output:
                        file_response(r,output,x="HTTPS")
                except requests.exceptions.RequestException as e:
                    print("\n**** EXCEPTION WITH HTTPS HOST: " + host.strip() + " ****\n")
                    print(str(e)+"\n")
                    output.write("\n**** EXCEPTION WITH HTTPS HOST: " + host.strip() + " ****\n")
                    output.write(str(e)+"\n")

if __name__ == "__main__":
    main()
