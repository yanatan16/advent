//
//  Day6.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/6/21.
//

import Foundation

struct Day6 : Solution {
    var exampleRawInput:String { """
3,4,3,1,2
""" }
    
    struct Input {
        let ages : [Int]
    }
    
    typealias Output = Int

    func parseInput(_ raw: String) -> Input {
        Input(
            ages: raw.components(separatedBy: "\n")
                .first!
                .components(separatedBy: ",")
                .compactMap { Int($0) }
        )
    }

    struct State {
        let ageCounts : [Int:Int]
        
        func ageBy1Day() -> State {
            State(ageCounts: [
                0:ageCounts[1, default:0],
                1:ageCounts[2, default:0],
                2:ageCounts[3, default:0],
                3:ageCounts[4, default:0],
                4:ageCounts[5, default:0],
                5:ageCounts[6, default:0],
                6:ageCounts[7, default:0] + ageCounts[0, default:0],
                7:ageCounts[8, default:0],
                8:ageCounts[0, default:0]
            ])
        }
        
        var total : Int {
            ageCounts.values.reduce(0) { $0 + $1 }
        }
    }
    
    func problem1(_ input: Input) -> Output {
        var state = State(ageCounts: input.ages.reduce(into: [:]) { (cnts, age) in
            cnts[age, default:0] += 1
        })
        
        (1...80).forEach { _ in
            state = state.ageBy1Day()
        }
        
        return state.total
    }
    
    func problem2(_ input: Input) -> Output {
        var state = State(ageCounts: input.ages.reduce(into: [:]) { (cnts, age) in
            cnts[age, default:0] += 1
        })
        
        (1...256).forEach { _ in
            state = state.ageBy1Day()
        }
        
        return state.total
    }
    
}

