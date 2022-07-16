from flight_computer import FlightComputer

def main(self):
    flight_computer = FlightComputer()
    flight_computer.startup()
    flight_computer.fly()
    print("flight complete")

if __name__ == "__main__":
    main()
    sys.exit(0)
