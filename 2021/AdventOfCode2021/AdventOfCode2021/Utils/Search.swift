//
//  Search.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/7/21.
//

import Foundation

func gradient<N:Numeric>(_ f: @escaping (N) -> N, diff: N) -> (N) -> N {
    { x in f(x+diff) - f(x) }
}

func binarySearchMinimize<N:BinaryInteger>(lower: N, upper: N, slope: (N) -> N) -> N {
    if lower == upper {
        return lower
    }
    
    let x = (lower + upper) / 2
    let m = slope(x)
    
    if m > 0 {
        return binarySearchMinimize(lower: lower, upper: x, slope: slope)
    } else if m < 0 {
        return binarySearchMinimize(lower: x + 1, upper: upper, slope: slope)
    } else {
        return x
    }

}
