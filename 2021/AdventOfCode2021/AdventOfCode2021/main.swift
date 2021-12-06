//
//  main.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/6/21.
//

import Foundation

let DEFAULT_DAY = "7"
let DEFAULT_INPUT_FILE = "/Users/joneisen/Downloads/advent/input\(DEFAULT_DAY).txt"

public func readInput(_ inputFile: String) throws -> String {
    return try! String(contentsOfFile: inputFile,
                       encoding: String.Encoding.utf8)
}

func main(day: String, inputFile: String) {
    let rawInput = try! readInput(inputFile)
    print("Read \(rawInput.count) characters from \(inputFile)")
    
    switch day {
    case "1":
        Day1().run(rawInput)
    case "2":
        Day2().run(rawInput)
    case "3":
        Day3().run(rawInput)
    case "4":
        Day4().run(rawInput)
    case "5":
        Day5().run(rawInput)
    case "6":
        Day6().run(rawInput)
    case "7":
        Day7().run(rawInput)
    default:
        print("Didn't find solution for \(day)")
        exit(1)
    }
}

let args = CommandLine.arguments.dropFirst()
let day : String = args.first ?? DEFAULT_DAY
let inputFile : String = args.dropFirst().first ?? DEFAULT_INPUT_FILE

main(day: day, inputFile: inputFile)
