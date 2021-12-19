//
//  Day19.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/17/21.
//

import Foundation

struct Day19 : Solution {
    var exampleRawInput: String { """
    --- scanner 0 ---
    404,-588,-901
    528,-643,409
    -838,591,734
    390,-675,-793
    -537,-823,-458
    -485,-357,347
    -345,-311,381
    -661,-816,-575
    -876,649,763
    -618,-824,-621
    553,345,-567
    474,580,667
    -447,-329,318
    -584,868,-557
    544,-627,-890
    564,392,-477
    455,729,728
    -892,524,684
    -689,845,-530
    423,-701,434
    7,-33,-71
    630,319,-379
    443,580,662
    -789,900,-551
    459,-707,401
    
    --- scanner 1 ---
    686,422,578
    605,423,415
    515,917,-361
    -336,658,858
    95,138,22
    -476,619,847
    -340,-569,-846
    567,-361,727
    -460,603,-452
    669,-402,600
    729,430,532
    -500,-761,534
    -322,571,750
    -466,-666,-811
    -429,-592,574
    -355,545,-477
    703,-491,-529
    -328,-685,520
    413,935,-424
    -391,539,-444
    586,-435,557
    -364,-763,-893
    807,-499,-711
    755,-354,-619
    553,889,-390
    
    --- scanner 2 ---
    649,640,665
    682,-795,504
    -784,533,-524
    -644,584,-595
    -588,-843,648
    -30,6,44
    -674,560,763
    500,723,-460
    609,671,-379
    -555,-800,653
    -675,-892,-343
    697,-426,-610
    578,704,681
    493,664,-388
    -671,-858,530
    -667,343,800
    571,-461,-707
    -138,-166,112
    -889,563,-600
    646,-828,498
    640,759,510
    -630,509,768
    -681,-892,-333
    673,-379,-804
    -742,-814,-386
    577,-820,562
    
    --- scanner 3 ---
    -589,542,597
    605,-692,669
    -500,565,-823
    -660,373,557
    -458,-679,-417
    -488,449,543
    -626,468,-788
    338,-750,-386
    528,-832,-391
    562,-778,733
    -938,-730,414
    543,643,-506
    -524,371,-870
    407,773,750
    -104,29,83
    378,-903,-323
    -778,-728,485
    426,699,580
    -438,-605,-362
    -469,-447,-387
    509,732,623
    647,635,-688
    -868,-804,481
    614,-800,639
    595,780,-596
    
    --- scanner 4 ---
    727,592,562
    -293,-554,779
    441,611,-461
    -714,465,-776
    -743,427,-804
    -660,-479,-426
    832,-632,460
    927,-485,-438
    408,393,-506
    466,436,-512
    110,16,151
    -258,-428,682
    -393,719,612
    -211,-452,876
    808,-476,-593
    -575,615,604
    -485,667,467
    -680,325,-822
    -627,-443,-432
    872,-547,-609
    833,512,582
    807,604,487
    839,-516,451
    891,-625,532
    -652,-548,-490
    30,-46,-14
    """}
    
    struct Scanner:CustomStringConvertible {
        let num: Int
        var beacons: [ThreeDPoint]
        var location: ThreeDPoint? = nil
        
        typealias PairDistance = (i: Int, j: Int, distance: Double)
        
        var distances: [(i: Int, j: Int, distance: Double)] {
            beacons.indices.map{$0}.pairs().map { (i,j) in
                (i, j, (beacons[i] - beacons[j]).magnitude)
            }
        }
        
        var description: String {
            "Scanner \(num): \n \(beacons)"
        }
        
        func rotate(_ rot: ThreeDPoint.Rotation) -> Scanner {
            var scanner = Scanner(num:num, beacons: beacons.map { $0.rotate(rot) })
            scanner.location = location
            return scanner
        }
        
        func sharedNodes(other: Scanner) -> [(Int, Int)] {
            let others = Dictionary(grouping: other.distances, by: { $0.distance } )
            
            var links: [Int:[Int]] = [:]
            
            self.distances.forEach { mine in
                others[mine.distance, default:[]].forEach { other in
                    links[mine.i, default:[]] += [other.i, other.j]
                    links[mine.j, default:[]] += [other.i, other.j]
                }
            }
            
            // print("links: \(links)")
            
            return links.compactMap { (myIndex, linkedIndices) in
                let freqs = linkedIndices.frequencies()
                // print("linked indices \(myIndex): \(freqs)")
                
                guard let matchingOtherIndex = freqs.filter({ (otherIndex, linkedIndices) in
                    linkedIndices >= 11
                }).keys.first
                else { return nil }
                
                // print("Found match (\(myIndex),\(matchingOtherIndex))")
                
                return (myIndex, matchingOtherIndex)
            }
            
        }
    }
    typealias Input = [Scanner]
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        raw.split2lines().enumerated().map { (i, scanner) in
            let beacons:[ThreeDPoint] = scanner.splitlines().dropFirst().map { line in
                let xs = line.components(separatedBy: ",").map{ Int($0)! }
                return ThreeDPoint(xs[0], xs[1], xs[2])
            }
            return Scanner(num: i, beacons: beacons)
        }
    }
    
    func findRotationAndPosition(sharedNodes: [(ThreeDPoint, ThreeDPoint)]) -> (ThreeDPoint.Rotation,ThreeDPoint)? {
        let validRotations:[(ThreeDPoint.Rotation, ThreeDPoint)] = ThreeDPoint.allRotations.compactMap { rot in
            // print("Rotation: \(rot)")
            let diffs = sharedNodes.map { (from, to) in
                from - to.rotate(rot) // = relpos
                // from = relpos - ro.rotate(rot)
            }
            // print("Diffs: \(diffs)")
            
            let diffFreq = diffs.frequencies().filter{ (_,v) in v >= 12 }
            if diffFreq.count == 1 {
                // print("Found rotation! \(rx), \(ry), \(rz)")
                return (rot, diffFreq.keys.first!)
            } else {
                return nil
            }
        }
        // print("Valid Rotations \(validRotations)")
        
        return validRotations.first
    }
    
    func solve(_ input: Input) -> [Scanner] {
        var scannersLeft = input.dropFirst().map{$0}
        var scanners = [input[0]]
        scanners[0].location = ThreeDPoint(0,0,0)
        
        while !scannersLeft.isEmpty {
            var breakNow = false
            for known in scanners {
                for (i, unknown) in scannersLeft.enumerated() {
                    let shared = known.sharedNodes(other: unknown)
                    
                    if shared.count >= 12 {
                        // print("evaluating pair \(known.num)->\(unknown.num)")
                        // Found a pair of scanners to map.
                        let sharedNodesPositions = shared.map { (i,j) in
                            (known.beacons[i], unknown.beacons[j])
                        }
                        guard let (rot, relpos) = findRotationAndPosition(sharedNodes: sharedNodesPositions)
                        else {
                            print("failed to find rotation/position for \(known.num)->\(unknown.num)")
                            print("positions \(sharedNodesPositions)")
                            return []
                        }
                        
                        // print("Scanner \(unknown.num) is in location \(relpos) and rotated \(rot)")
                        
                        var rotatedScanner = Scanner(
                            num: unknown.num,
                            beacons: unknown.beacons.map { b in
                                relpos + b.rotate(rot)
                            }
                        )
                        rotatedScanner.location = relpos
                        
                        // print("rotated scanner \(rotatedScanner.num) (Rel to \(known.num)): \(rotatedScanner.beacons)")
                        
                        scanners = [rotatedScanner] + scanners
                        scannersLeft.remove(at: i)
                        
                        breakNow = true
                        break
                    }
                }
                if breakNow { break }
            }
        }
        
        return scanners
    }
    
    func problem1(_ input: Input) -> Int {
        // print("input \(input)")
        
        
        return Set(solve(input).flatMap { $0.beacons }).count
    }
    
    func problem2(_ input: Input) -> Int {
        solve(input).pairs().map { (s0, s1) in (s0.location! - s1.location!).manhattenDistance }.max()!
    }
}
