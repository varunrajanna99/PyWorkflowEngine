import argparse
  
def main():

    parser = argparse.ArgumentParser(
        prog ='example_bot',
        description ='This is a simple bot'
    )

    parser.add_argument('--name', help ='Please provide your name')
    parser.add_argument('--list', help ='Please provide a list')
  
    args = parser.parse_args()
  
    if args.name:
        print(args.name)
  
    return (True, 'success')

main()