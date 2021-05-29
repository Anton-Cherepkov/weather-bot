from typing import List
import requests
from typing import Optional
from omegaconf import DictConfig, ListConfig


class WeatherReciever:
    def __init__(self, cfg: DictConfig):
        self._api_url: str = cfg.api_url
        self._token: str = cfg.token
        self._lang: str = cfg.lang
        self._places: ListConfig = cfg.places
        self._dangerous_conditions_decodings = cfg.dangerous_conditions_decodings
        self._forecast_parts_decondings = cfg.forecast_parts_decondings

    def _parse_condition(self, condition: str) -> str:
        if condition in self._dangerous_conditions_decodings:
            return f"Осторожно ⚠ {self._dangerous_conditions_decodings[condition]}"
        return f"Без осадков и прочей фигни 😉"
    
    def _request_weather_json(self, place: DictConfig) -> Optional[dict]:
        weather_request = requests.get(
            self._api_url,
            params={
                "lat": place.lat,
                "lon": place.lon,
                "lang": self._lang,
            },
            headers={
                "X-Yandex-API-Key": self._token,
            }
        )

        if weather_request.status_code == 200:
            return weather_request.json()

    def _parse_weather_json(self, weather_json: Optional[dict]) -> str:
        if weather_json:
            weather_str = str()
            weather_str += f"Сейчас: "
            weather_str += f"{self._parse_condition(weather_json['fact']['condition'])}.\n"
            for part in weather_json["forecast"]["parts"]:
                weather_str += f"{self._forecast_parts_decondings[part['part_name']]}: "
                weather_str += f"{self._parse_condition(part['condition'])}.\n"
            return weather_str
        else:
            return "Не удалось получить погоду :("
    
    def get_weather_for_all_places(self) -> List[str]:
        weather_strings: List[str] = list()

        for place in self._places:
            current_string = str()
            current_string += f"Погода для *{place.name}*:\n\n"
            current_string += self._parse_weather_json(
                weather_json=self._request_weather_json(place)
            )

            weather_strings.append(current_string)
        
        return weather_strings
