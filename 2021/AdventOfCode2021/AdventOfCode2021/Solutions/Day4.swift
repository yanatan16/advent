//
//  Day4.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/6/21.
//

import Foundation

struct Day4 : Solution {
    var exampleRawInput: String { """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""}
    
    typealias Board = [[Int]]
    struct Input {
        let boards : [Board]
        let drawings : [Int]
    }
    
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        let sections = raw.components(separatedBy: "\n\n")
        
        let drawings = sections.first!.split(separator: ",").compactMap { Int($0) }
        let boards = sections.dropFirst().map { board in
            board.split(whereSeparator: \.isNewline).compactMap { line in
                line.split(whereSeparator: \.isWhitespace).compactMap { Int($0) }
            }
        }
          
        return Input(boards: boards, drawings: drawings)
    }
    
    class BoardState {
        let board : Board
        var positionLookup : [Int:(Int,Int)] = [:]
        var rowMarks = [0,0,0,0,0]
        var colMarks = [0,0,0,0,0]
        var numbersToDraw : Set<Int> = Set()
        
        init(board: Board) {
            self.board = board
            board.enumerated().forEach { (i, row) in
                row.enumerated().forEach { (j, el) in
                    positionLookup[el] = (i,j)
                    numbersToDraw.insert(el)
                }
            }
        }
        
        func hasWon() -> Bool {
            !(rowMarks + colMarks).filter { $0 == 5 }.isEmpty
        }
        
        func draw(_ drawn: Int) {
            if let position = positionLookup[drawn] {
                rowMarks[position.0] += 1
                colMarks[position.1] += 1
                numbersToDraw.remove(drawn)
            }
        }
        
        func winningScore() -> Int {
            numbersToDraw.reduce(0) { $0 + $1 }
        }
    }
    
    func problem1(_ input: Input) -> Int {
        let states = input.boards.map(BoardState.init)
        
        for drawn in input.drawings {
            for state in states {
                state.draw(drawn)
            }
            
            if let won = states.filter({ $0.hasWon() }).first {
                return won.winningScore() * drawn
            }
        }
        return -1
    }
    
    func problem2(_ input: Input) -> Int {
        var states = input.boards.map(BoardState.init)
        
        for drawn in input.drawings {
            for state in states {
                state.draw(drawn)
            }
            
            let nextStates = states.filter({ !$0.hasWon() })
            
            if states.count == 1 && nextStates.count == 0 {
                let loss = states.first!
                return loss.winningScore() * drawn
            }
            
            states = nextStates
        }
        return -1
    }
}
