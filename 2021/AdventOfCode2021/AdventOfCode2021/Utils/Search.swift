//
//  Search.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/7/21.
//

import Foundation

func binarySearchMinimize(lower: Int, upper: Int, f: (Int) -> Int) -> (x: Int, y: Int) {
    if lower == upper {
        return (lower, f(lower))
    } else if lower + 1 == upper {
        let lpair = (lower, f(lower))
        let upair = (upper, f(upper))
        if lpair.1 > upair.1 {
            return upair
        } else {
            return lpair
        }
    }
            
    let x1 = (lower + upper) / 2
    let x2 = x1 + 1
    let y1 = f(x1)
    let y2 = f(x2)
    
    if y1 < y2 {
        return binarySearchMinimize(lower: lower, upper: x1, f: f)
    } else {
        return binarySearchMinimize(lower: x2, upper: upper, f: f)
    }

}
