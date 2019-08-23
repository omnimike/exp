{
    toVisitUp: function(elevator, currentFloor) {
        currentFloor = currentFloor === undefined ? elevator.currentFloor() : currentFloor;
        const toVisit = new Set();
        const pressedFloors = elevator.getPressedFloors();
        for (const floorNum of pressedFloors) {
            toVisit.add(floorNum);
        }
        for (const floorNum of this.upFloors) {
            toVisit.add(floorNum);
        }
        return Array.from(toVisit)
            .filter(floorNum => floorNum >= currentFloor)
            .sort();
    },
    toVisitDown: function(elevator, currentFloor) {
        currentFloor = currentFloor === undefined ? elevator.currentFloor() : currentFloor;
        const toVisit = new Set();
        const pressedFloors = elevator.getPressedFloors();
        for (const floorNum of pressedFloors) {
            toVisit.add(floorNum);
        }
        for (const floorNum of this.downFloors) {
            toVisit.add(floorNum);
        }
        return Array.from(toVisit)
            .filter(floorNum => floorNum <= currentFloor)
            .sort()
            .reverse();
    },
    requeueElevator: function(elevator) {
        let going;
        if (elevator.goingUpIndicator()) {
            const goingUp = this.toVisitUp(elevator, elevator.currentFloor());
            const goingDown = this.toVisitDown(elevator, goingUp[goingUp.length - 1]);
            going = goingUp.concat(goingDown);
        } else if (elevator.goingDownIndicator()) {
            const goingDown = this.toVisitDown(elevator, elevator.currentFloor());
            const goingUp = this.toVisitUp(elevator, goingDown[goingDown.length - 1]);
            going = goingDown.concat(goingUp);
        }
        elevator.destinationQueue = going;
        elevator.checkDestinationQueue();
    },
    requeueElevators: function(elevators) {
        for (const elevator of elevators) {
            this.requeueElevator(elevator);
        }
    },
    init: function(elevators, floors) {
        this.upFloors = new Set();
        this.downFloors = new Set();
        for (const floor of floors) {
            floor.on('up_button_pressed', () => {
                this.upFloors.add(floor);
                this.requeueElevators(elevators);
            });
            floor.on('down_button_pressed', () => {
                this.downFloors.add(floor);
                this.reqeueElevators(elevators);
            });
        }
        for (const elevator of elevators) {
            elevator.goingUpIndicator(true);
            elevator.goingDownIndicator(false);
            elevator.on('stopped_at_floor', (floorNum) => {
                if (elevator.goingUpIndicator()) {
                    this.upFloors.delete(floorNum);
                }
                if (elevator.goingDownIndicator()) {
                    this.downFloors.delete(floorNum);
                }
                this.requeueElevators(elevators);
                // todo change the indicators
            });
            elevator.on('floor_button_pressed', (floorNum) => {
                this.requeueElevator(elevator);
            });
        }
    },
    update: function(dt, elevators, floors) {
        // We normally don't need to do anything here
    }
}
