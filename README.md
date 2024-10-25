<p align="center">
  <a href="https://github.com/1nfocalypse/Snow">
	<img alt="Corto" src="https://i.imgur.com/dqequn9.png"/>
  </a>
</p>
<p align="center">
  <a href="https://choosealicense.com/licenses/mit/">
  	<img alt="License: MIT" src="https://img.shields.io/github/license/1nfocalypse/Snow"/>
  </a>
</p>
<h2 align="center">Snow</h3>
<h3 align="center">
  A Multithreaded Python3 Implementation of Miller-Rabin Probabilistic Primality Testing
</h2>
<p align="center">
  By <a href="https://github.com/1nfocalypse">1nfocalypse</a>
</p>

## What is it?
Snow is an implementation of Miller-Rabin probabilistic primality testing, in which candidate numbers are determined to either be composite or probably prime. This is primarily of relevance for large numbers, where prime determination becomes significantly harder. While algorithmically possible to determine primality in polynomial time,
the algorithms used to do so often hold significant overhead, limiting their applicability significantly. As such, probabilistic methods are typically employed. Snow is capable of enumerating probable primes for arbitrary bitlengths, with user-controllable variables for certainty, bitlength, the desired number of primes, and the number of threads
that a user desires to utilize. This is especially useful for user generation of RSA moduli, or any other case in which a very large prime is needed. It additionally tests all generated probable primes against the RSA-1024 modulus by default, since I am mostly interested in generating my own RSA-1024 modulus and wanted to test my luck, although 
this can easily be changed to fit end user preference.

## Usage
Snow is primarily meant to serve more as a script than an application. It can be ran by simply invoking it with Python3's interpreter, and customized by altering constants within the script itself.

## The Algorithm
Given an odd integer $n : n > 2$, form $n-1$ as $2^{s}d$, where $s \in \mathbb{N}$ and $d$ is odd. Consider an integer $a$ coprime to $n$, dubbed a base. $n$ is said to be a strong probable prime to base $a$ if either
- $a^{d} \equiv 1\mod n$
- $a^{2^{r}d} \equiv -1\mod n$ for some $r : 0 \leq r < s$
 We then simply check the relations, and for each value of $r$, the value of the expression may be calculated using the previous value $r$ by squaring over the field of characteristic $n$.

This is based off of Fermat's Little Theorem, $a^{n-1} \equiv 1\mod n$, hence the naming of $a$ to be a base. However, this does not assert primality, only that it is a strong probable prime to base $a$. However, unlike Fermat primality testing, there are no strong pseudoprimes for all values of $a$. Thus, by utilizing multiple values of $a$, 
we are able to state that a number is very likely to be prime should the congruence relation hold for all tested values of $a$. However, especially should the number of rounds be small, the chances of a strong pseudoprime being passed as a probable prime despite being composite is higher.

## Further Reading and References
- [Miller-Rabin Primality Test - Wikipedia](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test)
- [Stanford University - Primality Tests](https://crypto.stanford.edu/pbc/notes/numbertheory/millerrabin.html)
