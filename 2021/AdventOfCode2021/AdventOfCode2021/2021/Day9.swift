//
//  Day9.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/6/21.
//

import Foundation

// Started at 3:47
// part 1 at 3:59 (time: 12m)
// 18min phone call
// part 2 at 4:45 (time: 40m)

struct Day9 : Solution {
    var exampleRawInput: String { """
2199943210
3987894921
9856789892
8767896789
9899965678
"""}
    
    typealias Row = [Int]
    typealias Input = [Row]
    
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        raw.splitlines()
            .filter { $0.count > 0 }
            .map { row in
            row.map { Int(String($0))! }
        }
    }
    
    func problem1(_ input: Input) -> Int {
        Point.points(input)
            .filter { p in p.isLowPoint(input) }
            .map { p in p.value(input) }
            .map { h in h + 1 }.sum()
    }
    
    struct Point:Hashable,CustomStringConvertible {
        let i:Int
        let j:Int
        
        var description: String {
            "Point(\(i),\(j))"
        }
        static func points(_ input: Input) -> [Point] {
            input.indices.flatMap { i in
                input[0].indices.map { j in
                    Point(i:i,j:j)
                }
            }
        }
        
        func value(_ input: Input) -> Int {
            input[i][j]
        }
        
        func neighbors(_ input: Input) -> [Point] {
            let cols:Int = input.count
            let rows:Int = input[0].count
            return [(i-1,j),(i+1,j),(i,j-1),(i,j+1)].filter { (ii,jj) in
                ii >= 0 && ii < cols &&
                jj >= 0 && jj < rows
            }.map { (ii,jj) in
                Point(i:ii,j:jj)
            }
        }

        func isLowPoint(_ input: Input) -> Bool {
            let h = value(input)
            return neighbors(input).filter { p in
                p.value(input) <= h
            }.count == 0
        }
    }
    
    func basinSize(_ input: Input, p: Point) -> Int {
        var all :Set<Point> = Set()
        var next : Set<Point> = Set([p])
        
        while next.count > 0 {
            let p = next.popFirst()!
            // print("basinSize", p, p.value(input), next)
            if p.value(input) == 9 {
                continue
            } else {
                all.insert(p)
                next = next.union(p.neighbors(input)).subtracting(all)
            }
        }
        
        return all.count
    }
    
    func problem2(_ input: Input) -> Int {
        let basins = Point.points(input).filter { p in
            p.isLowPoint(input)
        }.map { p in
            basinSize(input, p:p)
        }
        
        return basins.sorted()[(basins.count-3)...].reduce(1) { $0 * $1 }
    }
}
