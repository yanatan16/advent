import Foundation

public struct Input {
    public let ages : [Int]
}
public typealias Output = Int

public func parseInput(_ raw: String) -> Input {
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

public enum Day6 {
    public static func problem1(_ input: Input) -> Output {
        var state = State(ageCounts: input.ages.reduce(into: [:]) { (cnts, age) in
            cnts[age, default:0] += 1
        })
        
        (1...80).forEach { _ in
            state = state.ageBy1Day()
        }
        
        return state.total
    }
    
    public static func problem2(_ input: Input) -> Output {
        var state = State(ageCounts: input.ages.reduce(into: [:]) { (cnts, age) in
            cnts[age, default:0] += 1
        })
        
        (1...256).forEach { _ in
            state = state.ageBy1Day()
        }
        
        return state.total
    }
    
}
