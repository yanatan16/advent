//
//  TwoD.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/14/21.
//

import Foundation

struct TwoDIndex : Hashable, CustomStringConvertible {
    let i:Int
    let j:Int
    
    var description: String {
        "2D<\(i),\(j)>"
    }
    init(_ i:Int, _ j:Int) {
        self.i = i
        self.j = j
    }
    
    func allNeighbors() -> [TwoDIndex] {
        [TwoDIndex(i-1,j-1),
         TwoDIndex(i-1,j),
         TwoDIndex(i-1,j+1),
         TwoDIndex(i,j-1),
         TwoDIndex(i,j+1),
         TwoDIndex(i+1,j-1),
         TwoDIndex(i+1,j),
         TwoDIndex(i+1,j+1),
        ]
    }
    
    func squareNeighbors() -> [TwoDIndex] {
        [TwoDIndex(i-1,j),
         TwoDIndex(i,j-1),
         TwoDIndex(i,j+1),
         TwoDIndex(i+1,j),
        ]
    }
}

extension Array where Element == Array<Int> {
    func twoDIndices() -> [TwoDIndex] {
        indices.flatMap { i in
            self[0].indices.map { j in
                TwoDIndex(i,j)
            }
        }
    }
    
    func safe2DGet(_ idx: TwoDIndex) -> Int? {
        if idx.i >= 0 && idx.i < count &&
            idx.j >= 0 && idx.j < self[0].count {
            return self[idx.i][idx.j]
        }
        return nil
    }

    mutating func safe2DUpdate(_ idx: TwoDIndex, _ f: (Int) -> Int) {
        if idx.i >= 0 && idx.i < count &&
            idx.j >= 0 && idx.j < self[0].count {
            self[idx.i][idx.j] = f(self[idx.i][idx.j])
        }
    }
    
    mutating func safe2DSet(_ idx: TwoDIndex, _ v: Int) {
        save2DUpdate(idx) { _ in v }
    }
}
