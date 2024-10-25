import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

#    _____
#   / ___/____  ____ _      __
#   \__ \/ __ \/ __ | | /| / /
#  ___/ / / / / /_/ | |/ |/ /
# /____/_/ /_/\____/|__/|__/
#
########################################################################################################################
# Snow is an implementation of Miller-Rabin probabalistic primality testing. It serves as a customizable script for
# generation of probable primes, and can be configured by altering the demarkated constants. After generating the
# desired number of primes, it will also analyze each of them to determine if it is a RSA factor, although this can
# quickly and easily be disabled if you're not generating primes in the suspected ranges of RSA factors. It is a
# multithreaded program, and while Python's multithreading leaves a lot to be desired, the feature is useful.
# Remember that numbers generated here are only likely to be prime, and a longer, more involved method must be used to
# verify primality (i.e. trial division). Notable in theory is AKS, which is a deterministic polynomial time algorithm
# that determines primality, but it's runtime is obscured by its big soft O of log(n)^6. It is what is referred to as a
# galactic algorithm, in the sense that it's asymptotic benefits only occur in problems of a galactic scale. The
# requisite overhead makes it otherwise infeasible and inferior in runtime to asymptotically inferior algorithms. Thus,
# for large numbers, Miller-Rabin testing is often utilized.
#
# Snow and all related aspects of it are licensed under the MIT license. For more information, consult the license.md
# file in the repository.
#
# Project Music Recommendation: Meakii - Memories (Trance) - https://www.youtube.com/watch?v=VkDOEHM2Xog
# Snow is taken from Neil Stephenson's description of randomness in bitmaps on Apple Macintosh crashes.
########################################################################################################################

# PRIME_SIZE -> Dictates the length of the random odd number. Guaranteed to be odd and have the specified set bit set.
PRIME_SIZE = 512
# DESIRED_NUM_PROB_PRIMES -> Dictates how many probable primes you would like to generate.
DESIRED_NUM_PROB_PRIMES = 10000
# THREADS -> The number of threads you would like to allocate to generating probable primes.
THREADS = 6
# ROUNDS -> The number of rounds of Miller-Rabin testing. More increases accuracy and runtime, and vice versa for less.
ROUNDS = 40

# globals
prob_primes = set()
RSAModulus = 135066410865995223349603216278805969938881475605667027524485143851526510604859533833940287150571909441798207282164471551373680419703964191743046496589274256239341020864383202110372958725762358509643110564073501508187510676594629205563685529475213500852879416377328533906109750544334999811150056977236890927563
mutex = threading.Lock()

def main():
    with ThreadPoolExecutor(max_workers = THREADS) as executor:
        futures = [executor.submit(find_probable_primes) for _ in range(THREADS)]
        for future in as_completed(futures):
            future.result()
    print("Dumping primes...")
    for prime in prob_primes:
        print("PRIME: " + str(prime))
        if (RSAModulus % prime == 0):
            print("RSA FACTOR: TRUE")
            exit(0)
        else:
            print("RSA FACTOR: FALSE")

def find_probable_primes():
    '''
    find_probable_primes()
    :return: void
    '''
    while len(prob_primes) < DESIRED_NUM_PROB_PRIMES:
        number = genRandomInt(PRIME_SIZE)
        if miller_rabin(number, ROUNDS):
            with mutex:
                prob_primes.add(number)
                print("Success. Found Prime #" + str(len(prob_primes)))

def miller_rabin(number, rounds):
    '''
    miller_rabin(number, rounds, prob_primes)
    :param number: potential prime
    :param rounds: rounds of evaluation (as n->inf, better perf)
    :param prob_primes: list of probable primes
    :return: bool (1 if prob prime, 0 else)
    '''
    r = 0
    s = number - 1
    while s % 2 == 0:
        r += 1
        s  = s >> 1
    nm1precomp = number - 1
    for _ in range(rounds):
        a = random.randint(2, nm1precomp)
        x = schneier_mult(a, s, number)
        if x == 1 or x == nm1precomp:
            continue
        for _ in range(r - 1):
            x = schneier_mult(x, 2, number)
            if x == nm1precomp:
                break
        else:
            return False
    return True


def genRandomInt(bits):
    '''
    genRandomInt(bits)
    :param bits: desired bitlength
    :return: odd bits length integer, with set bit bits = 1
    '''
    retStr = "1"
    for i in range(bits-2):
        retStr += str(random.randint(0, 4294967295) % 2)
    return int(retStr + "1", 2)

def schneier_mult(base, power, modulus):
    '''
    schneier_mult(base, power, modulus)
    :param base: base value
    :param power: exponent
    :param modulus: field characteristic
    :return: int
    '''
    r = 1
    while power != 0:
        if power & 1 == 1:
            r = (base * r) % modulus
        power = power >> 1
        base = (base * base) % modulus
    return r

# define entry point
if (__name__ == "__main__"):
    main()
