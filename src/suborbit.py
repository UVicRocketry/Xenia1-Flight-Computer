import csv
import numpy
import functools

# TODO: !MC - Possibly rename this because there is a class in the Xenia stuff
#       that has the same name. Maybe call this FlightData??
class DragData:
    """Storage of rocket information to be used for predictions.

    Fields
    ------
    cd_no_airbrakes_data:
      Drag coefficient with no airbrakes. Each element of the array is an array
      of mach number, cd area with power on, and cd area with no power.
    """

    def __init__(self, cd_no_airbrakes_path):
        """Initialize a new DragData object with the data specified.

        Panics
        ------
        The method will exit with status code 1 if any of the files could
        not be opened succesfully.

        Params
        ------
        cd_no_airbrakes_path:
            The path relative to program execution to the csv data for the
            coefficient of drag without airbrakes.
        """

        self.cd_no_airbrakes_data = []

        try:
            # Open the file.
            cd_no_airbrakes_file = open(cd_no_airbrakes_path, newline = '')

            cd_no_airbrakes_csv_reader = csv.reader(cd_no_airbrakes_file)
            # Store the data.
            for (i, row) in enumerate(cd_no_airbrakes_csv_reader):
                if i == 0:
                    continue
                self.cd_no_airbrakes_data.append(numpy.array(row).astype(float))

            # Close the files.
            cd_no_airbrakes_file.close()
        except:
            print("Couldn't open file")
            exit(1)

        self.cd_no_airbrakes_data.sort(key=functools.cmp_to_key(compare_drag_row))


def compare_drag_row(a, b):
    return a[0] - b[0]


def find_drag_coefficient(data, mach_number):
    """Binary search drag coefficient data.

    This could be accomplished with the bisect.bisect_left method in
    Python 3.10, but the Pi can only run 3.7 unless we complile from source.

    Params
    ------
    data:
      This should either be the cd_no_airbrakes_data array in a DragData object.

    mach_number:
      The desired mach number to look for.
    """
    if len(data) == 0:
        return [mach_number, 0.0, 0.0]

    if len(data) == 1:
        return data[0]

    index = int(len(data)/2)
    start = 0
    end = len(data)

    while end - start > 2:
        if data[index][0] < mach_number:
            start = index
        else:
            end = index

        index = int((end - start) / 2) + start

    return data[start]


class Suborbit:
    def __init__(self):
        self.data = DragData("drag_data/cda_no_airbrakes.csv")

    def run(alt, vel, accel):
        pass

################################################################################
# Tests
#
# TODO: Move tests to own file
################################################################################

def test_data_loading():
    data = DragData("drag_data/cda_no_airbrakes.csv")

def run_tests():
    test_data_loading()
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
