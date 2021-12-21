//
//  Day21.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/17/21.
//

import Foundation

protocol Dice {
    mutating func roll() -> Int
}

struct Day21 : Solution {
    var exampleRawInput: String { """
                Player 1 starting position: 4
                Player 2 starting position: 8
                """}
    
    struct Input {
        let player1Start: Int
        let player2Start: Int
    }
    typealias Output = BInt
    
    func parseInput(_ raw: String) -> Input {
        let split = raw.splitlines()
        return Input(
            player1Start: Int(split[0].components(separatedBy: "Player 1 starting position: ")[1])!,
            player2Start: Int(split[1].components(separatedBy: "Player 2 starting position: ")[1])!
        )
    }
    
    struct DeterministicDie : Dice {
        var rollCount = 0
        
        mutating func roll() -> Int {
            let r = (rollCount % 10) + 1
            rollCount = rollCount + 1
            return r
        }
    }
    
    func problem1(_ input: Input) -> BInt {
        // print("Input: \(input)")
        var dice = DeterministicDie()
        var state = Universe(
            p1i: input.player1Start-1,
            p1s: 0,
            p2i: input.player2Start-1,
            p2s: 0
        )
        
        while state.p1s < 1000 && state.p2s < 1000 {
            let interim = state.player1TurnWith(roll: dice.roll()+dice.roll()+dice.roll())
            if interim.p1s >= 1000 {
                break
            }
            state = interim.player2TurnWith(roll: dice.roll()+dice.roll()+dice.roll())
        }
        
        // print(state)
        
        // print("Game finished after \(dice.rollCount) rolls")
        // print(result)
        
        return BInt(min(state.p1s, state.p2s) * dice.rollCount)
    }
    
    static var probabilities: [Int:BInt] = [1,2,3].flatMap { roll1 in
        [1,2,3].flatMap { roll2 in
            [1,2,3].map { roll3 in
                roll1 + roll2 + roll3
            }
        }
    }.frequencies().mapValues { BInt($0) }
    
    struct Universe: Hashable, Equatable, CustomStringConvertible {
        let p1i:Int
        let p1s:Int
        let p2i:Int
        let p2s:Int
        
        var description: String {
            "Uni<\(p1i),\(p1s),\(p2i),\(p2s)>"
        }
        
        var complete: Bool {
            p1s >= 21 || p2s >= 21
        }
        
        static func ==(l: Self, r:Self) -> Bool {
            l.p1i == r.p1i && l.p1s == r.p1s &&
            l.p2i == r.p2i && l.p2s == r.p2s
        }
        
        func player1TurnWith(roll: Int) -> Universe {
            Universe(p1i: (p1i + roll) % 10,
                     p1s: p1s + 1 + (p1i + roll) % 10,
                     p2i: p2i,
                     p2s: p2s)
        }
        func player2TurnWith(roll: Int) -> Universe {
            Universe(p1i: p1i,
                     p1s: p1s,
                     p2i: (p2i + roll) % 10,
                     p2s: p2s + 1 + (p2i + roll) % 10)
        }
        
        func player1Turn() -> [(Universe, BInt)] {
            return probabilities.map { (roll, unicount) in
                (player1TurnWith(roll: roll),
                 unicount)
            }
        }
        
        func player2Turn() -> [(Universe, BInt)] {
            return probabilities.map { (roll, unicount) in
                (player2TurnWith(roll: roll),
                 unicount)
            }
        }
    }
    
    typealias Turn = (Universe) -> [(Universe, BInt)]
    func iterate(universes: [Universe:BInt], turn: Turn) -> (active: [Universe:BInt], wins: BInt) {
        let turned: [(Universe,BInt)] = universes.flatMap { (universe, unicount) -> [(Universe, BInt)] in
            turn(universe).map { (turnedUniverse, turnUnicount) in
                (turnedUniverse, unicount * turnUnicount)
            }
        }
        
        var wins:BInt = 0
        turned.filter { $0.0.complete }.forEach { (_, unicount) in
            wins += unicount
        }
        
        let active:[Universe:BInt] = turned.filter { !$0.0.complete }
            .reduce(into: [:]) { (m, pair) in
                m[pair.0, default: 0] += pair.1
            }
        
        return (active, wins)
    }
    
    func problem2(_ input: Input) -> BInt {
        // print("probabilities: \(probabilities)")
        
        let start = Universe(p1i: input.player1Start-1, p1s: 0,
                             p2i: input.player2Start-1, p2s: 0)
        
        var wins:[BInt] = [0,0]
        var universes:[Universe:BInt] = [start:1]
        
        while universes.count > 0 {
            let (active, p1wins) = iterate(universes: universes) { $0.player1Turn() }
            wins[0] += p1wins
            
            let (active2, p2wins) = iterate(universes: active) { $0.player2Turn() }
            wins[1] += p2wins
            
            universes = active2
        }
        
        return wins.max()!
    }
}
