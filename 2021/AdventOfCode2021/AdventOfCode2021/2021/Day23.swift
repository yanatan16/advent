//
//  Day23.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/17/21.
//

import Foundation

// start time 1:18
// part 1: 2:17:13 (0:59:13)
// part 2: 2:56:48 (1:38:48)
struct Day23 : Solution {
    var exampleRawInput: String { """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""}
    
    typealias Amphipod = Character
    typealias Room = (Amphipod, Amphipod)
    typealias Rooms = [Room]
    
    typealias Input = Rooms
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        let lines = raw.splitlines()
        let first = lines[2].components(separatedBy: "#").filter { $0.count > 0 }.map { $0.first! }
        let second = lines[3].trimmingCharacters(in: CharacterSet(charactersIn: " "))
            .components(separatedBy: "#")
            .filter { $0.count > 0 }
            .map { $0.first! }
        
        return zip(first, second).map { (f, s) in (f,s) }
    }
    
    enum Position : Hashable, Equatable, CustomStringConvertible {
        case hallway(Int)
        case room(Int, Int)
        
        static func ==(lhs: Self, rhs: Self) -> Bool {
            switch (lhs, rhs) {
            case (.hallway(let lx), .hallway(let rx)):
                return lx == rx
            case (.room(let lr, let ld), .room(let rr, let rd)):
                return lr == rr && ld == rd
            default:
                return false
            }
        }
        
        var description: String {
            switch self {
            case .hallway(let i):
                return "Hallway(\(i))"
            case .room(let room, let depth):
                return "Room(\(room),\(depth))"
            }
        }
        
        static let hallwayLowerBound = 0
        static let hallwayUpperBound = 10
        
        func distanceTo(_ other: Position) -> Int {
            switch (self, other) {
            case (.hallway(let x), .hallway(let y)):
                return abs(x-y)
            case (.room(let xr, let xd), _):
                return xd + other.distanceTo(Entryways[xr]!)
            case (_, .room(let yr, let yd)):
                return yd + self.distanceTo(Entryways[yr]!)
            }
        }
        
        func directionalRange(_ x: Int, _ y: Int) -> [Int] {
            if x <= y {
                return (x...y).map{$0}
            } else  {
                return (y...x).reversed().map{$0}
            }
        }
        
        func travel(to: Position) -> [Position] {
            switch (self, to) {
            case (.hallway(let x), .hallway(let y)):
                return directionalRange(x, y).map { .hallway($0) }
            case (.room(let xr, let xd), .room(let yr, let yd)):
                if xr == yr {
                    return directionalRange(xd, yd).map { .room(xr, $0) }
                } else {
                    let entryway = Day23.Entryways[xr]!
                    return directionalRange(xd, 1).map { .room(xr, $0) } +
                        entryway.travel(to: to)
                }
            case (.room(let xr, let xd), .hallway(_)):
                let entryway = Day23.Entryways[xr]!
                return directionalRange(xd, 1).map { .room(xr, $0) } +
                    entryway.travel(to: to)
            case (_, .room(let yr, let yd)):
                let entryway = Day23.Entryways[yr]!
                return self.travel(to: entryway) +
                    directionalRange(1, yd).map { .room(yr, $0) }
            }
        }
    }
    
    static let Entryways: [Int:Position] = [
        1:.hallway(2),
        2:.hallway(4),
        3:.hallway(6),
        4:.hallway(8)
    ]
    
    static let TravelCost:[Amphipod:Int] = [
        "A":1,
        "B":10,
        "C":100,
        "D":1000
    ]
    
    static let Homeroom:[Amphipod:Int] = [
        "A":1,
        "B":2,
        "C":3,
        "D":4
    ]
    
    enum AmphipodError : Error {
        case noAmphipodAtPosition(Position)
        case wrongAmphipodAtPosition(Position, expected: Amphipod, actual: Amphipod)
        case positionNotEmpty(Position, Amphipod)
        case podInTheWay(pod: Amphipod, from: Position, to: Position, inTheWayPod: Amphipod, inTheWayPos: Position)
    }
    
    struct State : CustomStringConvertible {
        typealias PodPair = (pod: Amphipod, pos: Position)
        var amphipods:[Position: Amphipod]
        var costTotal: Int
        
        var description: String {
            let hallway: String = (0...10).map { String(amphipods[.hallway($0), default: "."]) }.joined()
            let rooms: [String] = (1...4).map { depth in
                (1...4).map { room in
                    String(amphipods[.room(room,depth), default: "."])
                }.joined()
            }
            
            let topRows: [String] = [
                "State: (cost: \(costTotal))",
                "###########",
                "#" + hallway + "#"
            ]
            
            let bottomRows = ["  #########  "]
            
            let roomRows:[String] = (1...4).map { depth in
                if depth == 1 {
                    return "###" + rooms[depth-1].map{String($0)}.joined(separator: "#") + "###"
                } else {
                    return "  #" + rooms[depth-1].map{String($0)}.joined(separator: "#") + "#"
                }
                    
            }
        
            return (topRows + roomRows + bottomRows).joined(separator: "\n")
        }
        
        init(part1 input: Input) {
            costTotal = 0
            let pods : [PodPair] = input.enumerated().flatMap { (i, pods) -> [PodPair] in
                [(pods.0, Position.room(i+1, 1)),
                 (pods.1, Position.room(i+1, 2))]
            }
                
            amphipods = pods.reduce(into: [:]) { (m, pair) in
                m[pair.pos] = pair.pod
            }
        }
        
        static let Part2Pods:[PodPair] = [
            ("D", .room(1,2)),
            ("D", .room(1,3)),
            ("C", .room(2,2)),
            ("B", .room(2,3)),
            ("B", .room(3,2)),
            ("A", .room(3,3)),
            ("A", .room(4,2)),
            ("C", .room(4,3))
        ]
        
        init(part2 input: Input) {
            costTotal = 0
            let pods : [PodPair] = input.enumerated().flatMap { (i, pods) -> [PodPair] in
                [(pods.0, Position.room(i+1, 1)),
                 (pods.1, Position.room(i+1, 4))]
            } + Self.Part2Pods
                
            amphipods = pods.reduce(into: [:]) { (m, pair) in
                m[pair.pos] = pair.pod
            }
        }
        
        mutating func move(_ pod: Amphipod, _ from: Position, _ to: Position) throws {
            guard let podInPos = amphipods[from]
            else {
                throw AmphipodError.noAmphipodAtPosition(from)
            }
            
            if podInPos != pod {
                throw AmphipodError.wrongAmphipodAtPosition(from, expected: pod, actual: podInPos)
            }
            
            if amphipods[to] != nil {
                throw AmphipodError.positionNotEmpty(to, amphipods[to]!)
            }
            
            let travelPositions = from.travel(to: to).dropFirst()
            for pos in travelPositions {
                if let podInTheWay = amphipods[pos] {
                    throw AmphipodError.podInTheWay(pod: pod, from: from, to: to, inTheWayPod: podInTheWay, inTheWayPos: pos)
                }
            }
            
            amphipods.removeValue(forKey: from)
            amphipods[to] = pod
            costTotal += Day23.TravelCost[pod]! * from.distanceTo(to)
        }
    }
    
    func handCalculatedMoves(_ inputState: State) throws -> State {
        var state = inputState
        
        try state.move("A", .room(2, 1), .hallway(1))
        
        try state.move("C", .room(4, 1), .hallway(5))
        try state.move("A", .room(4, 2), .hallway(9))
        try state.move("D", .room(3, 1), .room(4, 2))
        
        try state.move("B", .room(3, 2), .hallway(7))
        try state.move("C", .hallway(5), .room(3, 2))
        try state.move("C", .room(2, 2), .room(3, 1))
        
        try state.move("B", .hallway(7), .room(2, 2))
        try state.move("D", .room(1, 1), .room(4, 1))
        try state.move("B", .room(1, 2), .room(2, 1))
        
        try state.move("A", .hallway(9), .room(1, 2))
        try state.move("A", .hallway(1), .room(1, 1))
        
        return state
    }
    
    func problem1(_ input: Input) -> Int {
        if input[0].0 != "D" {
            print("Hand calculating result. Not doing example.")
            return -1
        }
        
        let state = State(part1: input)
        print(state)
        
        do {
            let resultState = try handCalculatedMoves(state)
            print(resultState)
            
            return resultState.costTotal
        } catch (let e) {
            print("Error! \(e)")
            print(state)
            return -1
        }
    }
    
    func problem2(_ input: Input) -> Int {
        if input[0].0 != "D" {
            print("Hand calculating result. Not doing example.")
            return -1
        }
        
        var state = State(part2: input)
        print(state)
        
        do {
            try state.move("C", .room(4,1), .hallway(10))
            try state.move("A", .room(4,2), .hallway(0))
            try state.move("C", .room(4,3), .hallway(9))
            try state.move("A", .room(4,4), .hallway(1))
            
            try state.move("D", .room(3,1), .room(4, 4))
            try state.move("D", .room(1,1), .room(4, 3))
            try state.move("D", .room(1,2), .room(4, 2))
            try state.move("D", .room(1,3), .room(4, 1))
            
            // Don't know if this is minimal
            try state.move("B", .room(1, 4), .hallway(7))
            try state.move("A", .room(2, 1), .room(1, 4))
            try state.move("A", .hallway(1), .room(1, 3))
            try state.move("A", .hallway(0), .room(1, 2))
            
            try state.move("B", .room(3, 2), .hallway(0))
            try state.move("A", .room(3, 3), .room(1, 1))
            try state.move("B", .room(3, 4), .hallway(1))
            
            try state.move("C", .room(2, 2), .room(3, 4))
            try state.move("B", .room(2, 3), .hallway(3))
            try state.move("C", .room(2, 4), .room(3, 3))
        
            try state.move("B", .hallway(7), .room(2, 4))
            try state.move("B", .hallway(3), .room(2, 3))
            try state.move("B", .hallway(1), .room(2, 2))
            try state.move("B", .hallway(0), .room(2, 1))
            
            try state.move("C", .hallway(9), .room(3, 2))
            try state.move("C", .hallway(10), .room(3, 1))
        
            print(state)
        
            // 40974 is too high
            // 40934 is too low
            // 40954 is just right
            return state.costTotal
        } catch (let e) {
            print("Error! \(e)")
            print(state)
            return -1
        }
    }
}
