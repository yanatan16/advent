//
//  Extensions.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/6/21.
//

import Foundation

extension Array where Element: Collection {
    func transpose() -> Array<Array<Element.Element>> {
        self.first!.indices.map { index in
            self.map { row in row[index] }
        }
    }
}

extension Array where Element : Numeric {
    func sum() -> Element {
        reduce(Element.zero, { $0 + $1 })
    }
}

func twoToThePowerOf(_ exp: Int) -> Int {
    Int(pow(2.0, Double(exp)))
}