//
//  Day25.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/17/21.
//

import Foundation

struct Day25 : Solution {
    var exampleRawInput: String { """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""}
    
    enum LocationState {
        case down
        case east
        case empty
    }
    
    typealias Input = [[LocationState]]
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        raw.splitlines().map { line in
            line.map { char in
                switch char {
                case ">":
                    return .east
                case "v":
                    return .down
                default:
                    return .empty
                }
            }
        }
    }
    
    struct State : CustomStringConvertible {
        var easts:Set<TwoDIndex>
        var downs:Set<TwoDIndex>
        let rows: Int
        let cols: Int
        
        var description: String {
            (0...(rows-1)).map { i in
                (0...(cols-1)).map { j in
                    if easts.contains(TwoDIndex(i,j)) {
                        return ">"
                    } else if downs.contains(TwoDIndex(i,j)) {
                        return "v"
                    } else {
                        return "."
                    }
                }.joined()
            }.joined(separator: "\n")
        }
        
        func isMovable(to: TwoDIndex) -> Bool {
            !(easts.contains(to) || downs.contains(to)) &&
            to.i < rows
        }
        
        mutating func stepEasts() -> Bool {
            var changed = false
            easts = Set(easts.map { cucumber in
                if isMovable(to: cucumber.wrappingRight(cols: cols)) {
                    changed = true
//                    print("moving \(cucumber) to \(cucumber.wrappingRight(cols: cols))")
                    return cucumber.wrappingRight(cols: cols)
                } else {
                    return cucumber
                }
            })
            return changed
        }
        
        mutating func stepDowns() -> Bool {
            var changed = false
            downs = Set(downs.map { cucumber in
                if isMovable(to: cucumber.wrappingDown(rows: rows)) {
                    changed = true
//                    print("moving \(cucumber) to \(cucumber.down())")
                    return cucumber.wrappingDown(rows: rows)
                } else {
                    return cucumber
                }
            })
            return changed
        }
        
        mutating func step() -> Bool {
            var changed = false
            changed = stepEasts() || changed
            changed = stepDowns() || changed
            return changed
        }
    }
    
    func problem1(_ input: Input) -> Int {
        print("input: \(input)")
        var state = State(
            easts: Set(input.enumerated().flatMap { (i,line) in
                line.enumerated().compactMap { (j,loc) in
                    switch loc {
                    case .east:
                        return TwoDIndex(i,j)
                    default:
                        return nil
                    }
                }
            }),
            downs: Set(input.enumerated().flatMap { (i,line) -> [TwoDIndex] in
                line.enumerated().compactMap { (j,loc) -> TwoDIndex? in
                    switch loc {
                    case .down:
                        return TwoDIndex(i,j)
                    default:
                        return nil
                    }
                }
            }),
            rows: input.count,
            cols: input[0].count
        )
        
        var steps = 0
        var changed = true

        while changed {
            changed = state.step()
            steps += 1
        }
        
        return steps
    }
    
    func problem2(_ input: Input) -> Int {
        -1
    }
}
