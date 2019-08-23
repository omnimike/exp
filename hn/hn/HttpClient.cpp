
#include <curl/curl.h>
#include <memory>

#include "HttpClient.h"

namespace hn {

std::unique_ptr<HttpResponse> HttpClient::get(const std::string &url) const {
  std::string bodyBuffer{};
  auto handle = curl_easy_init();
  curl_easy_setopt(handle, CURLOPT_URL, url.c_str());
  curl_easy_setopt(handle, CURLOPT_WRITEFUNCTION, HttpClient::write_data);
  curl_easy_setopt(handle, CURLOPT_WRITEDATA, &bodyBuffer);
  char error_string[CURL_ERROR_SIZE]{0};
  curl_easy_setopt(handle, CURLOPT_ERRORBUFFER, error_string);
  auto ret = curl_easy_perform(handle);
  if (ret != CURLE_OK) {
    throw HttpException(std::string{error_string});
  }
  return std::make_unique<HttpResponse>(bodyBuffer);
}

} // namespace hn
