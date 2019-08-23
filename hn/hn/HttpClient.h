
#ifndef HN_HTTPCLIENT_H_
#define HN_HTTPCLIENT_H_

#include <string>
#include <memory>
#include <exception>
#include <folly/json.h>

namespace hn {

class HttpResponse {
  public:
    HttpResponse(std::string &body) : body_(std::move(body)) {}

    const std::string& body() const {
      return body_;
    }

    const folly::dynamic json() const {
      return folly::parseJson(body_);
    }

  private:
    const std::string body_;
};

class HttpClient {
  public:
    std::unique_ptr<HttpResponse> get(const std::string &url) const;
  private:
    static std::size_t write_data(
      const void * const buffer,
      const std::size_t,
      const std::size_t nmemb,
      std::string * const res
    ) {
      res->append((char*)buffer, nmemb);
      return nmemb;
    }
};

class HttpException : public std::exception {
  public:
    HttpException(std::string msg) : msg_(std::move(msg)) {}
    virtual const char * what() const throw() {
      return msg_.c_str();
    }
  private:
    std::string msg_;
};

} // namespace hn

#endif  // HN_HTTPCLIENT_H_
