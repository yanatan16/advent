//
//  main.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/6/21.
//

import Foundation

let DEFAULT_DAY = "11"

func defaultInputFile(day: String) -> String { "\(FileManager().homeDirectoryForCurrentUser.path)/dev/jon/advent/2021/inputs/input\(day).txt"
}

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
        Day7Rewrite().run(rawInput)
    case "8":
        Day8().run(rawInput)
    case "9":
        Day9().run(rawInput)
    case "10":
        Day10().run(rawInput)
    case "11":
        Day11().run(rawInput)
    case "12":
        Day12().run(rawInput)
    case "13":
        Day13().run(rawInput)
    default:
        print("Didn't find solution for \(day)")
        exit(1)
    }
}

let args = CommandLine.arguments.dropFirst()
let day : String = args.first ?? DEFAULT_DAY
let inputFile : String = args.dropFirst().first ?? defaultInputFile(day: day)

main(day: day, inputFile: inputFile)
