//
//  Array.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/18/21.
//

import Foundation

extension Array {
    func pairs() -> [(Element, Element)] {
        enumerated().flatMap { (i, x) in
            self[(i+1)...].map { y in
                (x,y)
            }
        }
    }
}
