# Class diagram
Solid hollow triangle: extends. Dashed hollow triangle: implements. Filled diamond: facility owns its slots. Tickets reference one user and vehicle.

```mermaid
classDiagram
Vehicle <|-- TwoWheeler
Vehicle <|-- Car
Car <|-- ElectricCar
Chargeable <|.. ElectricCar
ParkingFacility *-- Slot
ParkingFacility o-- ParkingTicket
ParkingTicket --> Vehicle
ParkingTicket --> ParkingUser
ParkingUser --> Pass
Pass <|.. MonthlyPass
TwoWheeler <|-- EBike
Car <|-- DeliveryVan
Pass <|.. OneDayPass
ParkingFacility <|-- ExtendedFacility
ExtendedFacility --> PricingRule
PricingRule <|.. PeakVanRule
```

The DOT and SVG files show the original baseline; this Mermaid includes the Task12 additions. No production source under Task01 is changed for Task12.
