//
//  IterationPrinter.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/15/21.
//

import Foundation

struct IterationPrinter {
    var iter = 0
    let every:Int
    init() {
        self.every = 100
    }
    init(_ every: Int) {
        self.every = every
    }
    mutating func iterprint(_ s: String) {
        if (iter % every) == 0 {
            print("\(iter): \(s)")
        }
        iter += 1
    }
}
