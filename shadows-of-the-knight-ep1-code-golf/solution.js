/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

var inputs = readline().split(' ');
const W = parseInt(inputs[0]); // width of the building.
const H = parseInt(inputs[1]); // height of the building.
const N = parseInt(readline()); // maximum number of turns before game over.
var inputs = readline().split(' ');
const X0 = parseInt(inputs[0]);
const Y0 = parseInt(inputs[1]);

class Direction {
    direction;
    hor;
    ver;
    dHor;
    dVer;

    constructor(direction) {
        this.direction = direction;

        this.hor = [
            direction.includes('R') ? 'R' : '',
            direction.includes('L') ? 'L' : '',
        ].join('');

        this.ver = [
            direction.includes('U') ? 'U' : '',
            direction.includes('D') ? 'D' : '',
        ].join('');

        this.dHor = {
            '': 0,
            'L': -1,
            'R': 1,
        }[this.hor];

        this.dVer = {
            '': 0,
            'U': -1,
            'D': 1,
        }[this.ver];
    }

    getHorizontalRange(point, hRange) {
        if (this.hor === '') {
            return hRange;
        }

        return {
            'R': [point.x + 1, hRange[1]],
            'L': [hRange[0], point.x - 1],
        }[this.hor];
    }

    getVerticalRange(point, vRange) {
        if (this.ver === '') {
            return vRange;
        }

        return {
            'U': [vRange[0], point.y - 1],
            'D': [point.y + 1, vRange[1]],
        }[this.ver];
    }
}
class History {
    hLog = [];
    vLog = [];
    hSer = 0;
    vSer = 0;
    update(dir) {
        const vDir = dir.ver;
        const hDir = dir.hor;

        if (this.hLog.length > 0 && this.hLog[this.hLog.length - 1] === hDir) {
            this.hSer++;
        } else {
            this.hSer = 0;
        }

        if (this.vLog.length > 0 && this.vLog[this.vLog.length - 1] === vDir) {
            this.vSer++;
        } else {
            this.vSer = 0;
        }

        this.hLog.push(hDir);
        this.vLog.push(vDir);
    }
}

let point = {
    x: X0,
    y: Y0,
};

let hRange = [0, W - 1];
let vRange = [0, H - 1];

let isFirstJump = true;
const vDirHistory = [];
const hDirHistory = [];
const dirHistory = [];
const history = new History();


// game loop
while (true) {
    const bombDir = readline(); // the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
    const dir = new Direction(bombDir);

    dirHistory.push(bombDir);
    vDirHistory.push(dir.ver);
    hDirHistory.push(dir.hor);
    history.update(dir);

    hRange = dir.getHorizontalRange(point, hRange);
    vRange = dir.getVerticalRange(point, vRange);


    let x = hRange[0] + Math.round((hRange[1] - hRange[0]) / 2);
    let y = vRange[0] + Math.round((vRange[1] - vRange[0]) / 2);

    if (history.vSer >= 3) {
        let yDiv = 4 - (history.vSer - 2) * 0.2;
        yDiv = Math.max(2, yDiv);
        y = vRange[0] + Math.round((vRange[1] - vRange[0]) / 2) + dir.dVer * Math.round((vRange[1] - vRange[0]) / yDiv);
    }
    if (history.hSer >= 3) {
        let xDiv = 4 - (history.hSer - 2) * 0.2;
        xDiv = Math.max(2, xDiv);
        x = hRange[0] + Math.round((hRange[1] - hRange[0]) / 2) + dir.dHor * Math.round((hRange[1] - hRange[0]) / xDiv);
    }


    console.error({
        W,
        H,
        hRange,
        vRange,
        point,
        newPoint: {x, y}
    });

    // the location of the next window Batman should jump to.
    console.log(`${x} ${y}`);
    point = {x, y};
}
