
#include <iostream>
#include <curl/curl.h>
#include <folly/json.h>
#include <folly/format.h>
#include "HttpClient.h"

using namespace hn;

int main2() {
  curl_global_init(CURL_GLOBAL_ALL);
  HttpClient client{};
  auto res = client.get("https://hacker-news.firebaseio.com/v0/topstories.json");
  auto story_ids = folly::parseJson(res->body());
  for (auto& story_id : story_ids) {
    auto story_url = folly::sformat("https://hacker-news.firebaseio.com/v0/item/{}.json", story_id);
    auto story_res = client.get(story_url);
    auto story = folly::parseJson(story_res->body());
    std::cout << folly::toPrettyJson(story);
    break;
  }
  curl_global_cleanup();
  return 0;
}

struct A {
  std::string name_;
  A(std::string name) : name_(name) { std::cout << "building " << name_ << std::endl; }
  A(const A& other) : name_(other.name_ + " (copy)") {
    std::cout << "copying " << name_ << std::endl;
  }
  A(A&& other) : name_(other.name_ + " (moved)") { std::cout << "moving " << name_ << std::endl; }
  ~A() { std::cout << "destroying  " << name_ << std::endl; }
};

struct B {
  A a;
  B(A&& a) : a(std::move(a)) {
    std::cout << "B(A&& a)" << std::endl;
  }
  //B(const A& a) : a(a) {
  //  std::cout << "B(const A& a)" << std::endl;
  //}
};

struct F {
  A a;
  //F(std::unique_ptr<A>& a) : a(std::move(*a)) {
  //  std::cout << "F(std::unique_ptr<A>& a)" << std::endl;
  //}

  F(std::unique_ptr<A> a) : a(std::move(*a)) {
    std::cout << "F(std::unique_ptr<A>&& a)" << std::endl;
  }
};

int main() {
  std::cout << "------------" << std::endl;
  A a1("a1");
  B b1(std::move(a1));
  std::cout << "------------" << std::endl;
  B b2{A("a2")};
  std::cout << "------------" << std::endl;
  const A a3("a3");
  B b3{A{a3}};
  std::cout << "------------" << std::endl;

  std::cout << "------------" << std::endl;
  auto a8 = std::make_unique<A>("a8");
  F f1(std::move(a8));
  std::cout << "------------" << std::endl;
  F f2{std::make_unique<A>("a9")};
  std::cout << "------------" << std::endl;
}
