import Html exposing (Html, button, div, text, input)
import Html.Attributes exposing (type_)
import Html.Events exposing (onInput)
import String
import Graph

main =
  Html.beginnerProgram { model = model, view = view, update = update }


-- MODEL

type alias Model = { 
  amplitude: Float 
}

model : Model
model =
  {
    amplitude = 2
  }


-- UPDATE

type Msg = AmplitudeChange String

update : Msg -> Model -> Model
update msg model =
  case msg of
    AmplitudeChange val ->
      case (String.toFloat val) of
        Ok amp ->
          {model | amplitude = amp}
        _ ->
          model

-- VIEW

view : Model -> Html Msg
view model =
  div []
    [ Graph.graphIt (sinCurve model.amplitude)
    , input [type_ "range", onInput AmplitudeChange ] []
    ]

sinCurve: Float -> List Graph.Point
sinCurve amp =
  List.map (\x -> (toFloat x) / 4) (List.range 0 250)
  |> List.map sin
  |> List.indexedMap (\x v -> {x = (toFloat x*2), y = v * amp} )