module Graph exposing (..)

import Svg exposing (..)
import Svg.Attributes exposing (..)
import String

type alias Point = 
  { x: Float
  , y: Float
  }

graphIt : List Point -> Svg msg
graphIt points =
  let
    w = 500
    h = 300
  in
  svg 
  [ width (toString (w + 4))
  , height (toString (h + 4))
  , Svg.Attributes.style "margin: 10px;"
  ] [
    rect [
      x "2"
    , y "2"
    , width (toString w)
    , height (toString h)
    , fill "bisque"
    , rx "6"
    , ry "6"
    , stroke "firebrick"
    , strokeWidth "2"
    ] []
  , Svg.path [
      d (
        points
        |> scaleToBoard -100 100 h
        |> offsetByMargin 2 2
        |> pointsToPath
      )
    , stroke "navy"
    , strokeWidth "2"
    , fillOpacity "0"
    , Svg.Attributes.strokeLinejoin "round"
    ] []   
  ]


discretize: (Float -> Float) -> Int -> Float -> Float -> List Point
discretize f count size offset  =
    List.range 0 count -- Make n steps
    |> List.map (\n -> (toFloat n) * size - offset) -- Convert to floats
    |> List.map (\x -> {x = x, y = f x })


scaleToBoard: Float -> Float -> Float -> List Point -> List Point
scaleToBoard min max height points =
  let
    rangeY = height / (max - min)
    offsetY = max / (max - min) * height
  in
  List.map (\p -> {p | y = -p.y * rangeY + offsetY}) points
    

offsetByMargin:  Float -> Float -> List Point -> List Point
offsetByMargin x y points =
    List.map (\p -> {x = p.x + x, y = p.y + y}) points


pointsToPath: List Point -> String
pointsToPath points =
    "M" ++ (
        List.map pointToString points
        |> String.join "L" 
    )


pointToString: Point -> String
pointToString point =
    toString point.x ++ "," ++ toString point.y


scaleY: Float -> Float -> Float -> Float
scaleY value minimum maximum =
     clamp 0 1 (value / (abs minimum) + (abs maximum))
