//
//  TwoD.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/14/21.
//

import Foundation

struct TwoDIndex : Hashable, CustomStringConvertible, Equatable {
    let i:Int
    let j:Int
    
    init(_ i:Int, _ j:Int) {
        self.i = i
        self.j = j
    }
    
    static func ==(lhs: TwoDIndex, rhs: TwoDIndex) -> Bool {
        lhs.i == rhs.i && lhs.j == rhs.j
    }
    
    var description: String {
        "2D<\(i),\(j)>"
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
    
    static func generateIndices(rows: Int, cols: Int) -> [TwoDIndex] {
        (0...(rows-1)).flatMap { i in
            (0...(cols-1)).map { j in
                TwoDIndex(i,j)
            }
        }
    }
}

extension Array where Element == Array<Int> {
    func twoDIndices() -> [TwoDIndex] {
        TwoDIndex.generateIndices(
            rows: indices.count,
            cols: self[0].count
        )
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
        safe2DUpdate(idx) { _ in v }
    }
}
