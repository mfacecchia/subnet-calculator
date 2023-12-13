import math

def checkNetworkValue(network):
    '''Checks if the values input are valid for a network'''
    #TODO: Check for max value 223 in network class
    for byte in network:
        #Firstly, it tries if the values input can be converted in integer values, otherwise the function will return `False`, then it will check if the values are valid IP digits
        try:
            int(byte)
        except ValueError:
            return False
        else:
            if(int(byte) < 0 or int(byte) > 255):
                return False
    #Returns `True` if everything goes as expected
    return True


def checkNetworkClass(network, subnetMask):
    '''Checks the network class and relative subnet mask'''
    #Dictionary with all the network classes that can be divided in subnets
    networkClasses = {
        'A': [[1, 127], [255, 0, 0, 0]],
        'B': [[128, 191], [255, 255, 0, 0]],
        'C': [[192, 223], [255, 255, 255, 0]],
    }
    counter = 0
    #Checking if the Network IP and the relative Subnet mask are correct for the network chosen class
    for nwClassName, nwClassRange in networkClasses.items():
        if(network[0] >= nwClassRange[0][0] and network[0] <= nwClassRange[0][1]):
            if(subnetMask == nwClassRange[1]):
                print("Valid Network") 
                return [True]
        else:
            continue
    print("Invalid Network")
    #Returns the class name as well as the expected subnet mask value for that class
    return [nwClassName, nwClassRange[1]]
            

def changeNetworkAndSubnet(network, subnetMask, nwClass):
    '''Lets the user change Network IP or Subnet Mask'''
    print(f"\nThe Subnet Mask {'.'.join(map(str, subnetMask))} input does not match with the {nwClass[0]} class Subnet Mask for the Network {'.'.join(map(str, network))} (Subnet Mask {'.'.join(map(str, nwClass[1]))}).")
    
    newNetAndSubnet = input("\n\nPlease input valid IP Address and Subnet Mask values: ").replace(' ', '.').split('.')
    #With the `split()` function, the list expects 8 items, if it's longer or shorter, the value input is not correct and has to try again
    while(len(newNetAndSubnet) != 8):
        print("\nWrong input...")
        newNetAndSubnet = input("Input some valid IP Address and Subnet Mask values: ").replace(' ', '.').split('.')
    
    #Checking again if the network IP and Subnet Mask values are correctly input
    while(checkNetworkValue(newNetAndSubnet) == False):
        newNetAndSubnet = input("The Network input contains invalid values (lower than 0 and/or higher than 255) or wrong values were input, please try again: ").replace(' ', '.').split('.')

    newNet = newNetAndSubnet[:4]
    newSubnet = newNetAndSubnet[4:]
    #Pasring the network information from string to integer
    parseIP(newNet, newSubnet)

    #Checking again if the network IP and Subnet Mask class are correct
    nwClass = checkNetworkClass(newNet, newSubnet)
    
    if(len(nwClass) == 2):
        changeNetworkAndSubnet(newNet, newSubnet, nwClass)
    return([newNet, newSubnet])


def parseIP(network, subnetMask):
    '''Converts the `str` IP and Subnet Mask values in `int` type'''
    for byte in range(len(network)):
        network[byte] = int(network[byte])
        subnetMask[byte] = int(subnetMask[byte])
    

def subnetDataInput(subnetMask):
    '''Prompts the user to input the total number of hosts and the number of subnets in the network'''
    totalHosts = None
    subnetNumber = None

    while True:
        try:
            #Checks if the hosts number is already input, otherwise the program will ask the user to input it
            if(not isinstance(totalHosts, int)):
                totalHosts = int(input(f"\nInput the total number of hosts you expect to have in your Network (min 1 max {(2 ** (subnetMask.count(0) * 8)) - 3}): "))
                #Checks if the total hosts number input is correct (it cannot exceed a value expected by the network which is 2^n)
                while(totalHosts < 1 or totalHosts > ((2 ** (subnetMask.count(0) * 8)) - 3)):
                    totalHosts = None
                    totalHosts = int(input(f"\nPlease input a valid number of hosts between 1 and {(2 ** (subnetMask.count(0) * 8)) - 3}: "))
            #Same checks but for the number of subnets
            if(not isinstance(subnetNumber, int)):
                subnetNumber = int(input(f"\nHow many subnets do you want to create (min 1 max {255 * subnetMask.count(0)})? "))
                while(subnetNumber < 1 or subnetNumber > (255 * subnetMask.count(0))):
                    subnetNumber = None
                    subnetNumber = int(input(f"\nPlease input a valid subnets value between 1 and {255 * subnetMask.count(0)}: "))
        except ValueError:
            print("Wrong input...")
        else:
            break
    return([totalHosts, subnetNumber])


def main():

    network = input("Input the beginning Network (not yet subdivided) that you want to divide in Subnets, as well as the Network's Subnet Mask (separated by a space): ").replace(' ', '.').split('.')

    #With the `split()` function, the list expects 8 items, if it's longer or shorter, the value input is not correct and has to try again
    while(len(network) != 8):
        print("\nWrong input...")
        network = input("Please input the Network that you want to subdivide and the Network's Subnet Mask value (separated by a space): ").replace(' ', '.').split('.')

    #Checking if the IP and Subnet Mask network values are correctly input to proceed
    while(checkNetworkValue(network) == False):
        network = input("The Network or the Subnet Mask value contain unsupported values (lower than 0 and/or higher than 255) or a wrong value was input, please try again: ").replace(' ', '.').split('.')

    #Moving the subnet mask data to a dedicated list and deleting it from the network dedicated list
    subnetMask = network[4:]
    for sm in network[4:]:
        network.remove(sm)

    #Parsing the address from `str` to `int` value
    parseIP(network, subnetMask)

    #Checking if the input IP and Subnet Mask values have the same expected network class values
    nwClassResults = checkNetworkClass(network, subnetMask)
    
    #`len(nwClassResults) != 1` means that the network data were incostintent so it needs to be updated with the correct information
    if(len(nwClassResults) != 1):
        updatedNwSm = changeNetworkAndSubnet(network, subnetMask, nwClassResults)
        #Moving the updated data from the function to the dedicated network lists and then parsing the data to `int`
        network = updatedNwSm[0]
        subnetMask = updatedNwSm[1]
        parseIP(network, subnetMask)

    subnetData = subnetDataInput(subnetMask)

    print(subnetData)   

    #NOTE: Calculate the power of subnets  (magic number calculation) by using math.log(subnetData[1], 2)


if __name__ == '__main__':
    main() 