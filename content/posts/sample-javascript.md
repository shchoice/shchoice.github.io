+++
date = '2026-03-14T09:00:00+09:00'
draft = false
title = 'JavaScript 모던 문법 정리'
categories = ['JavaScript']
tags = ['javascript', 'es6', 'frontend']
description = 'ES6 이후의 모던 JavaScript 문법을 정리합니다.'
+++

## 모던 JavaScript란?

ES6(ECMAScript 2015) 이후 JavaScript는 더욱 강력하고 표현력 있는 언어가 되었습니다.
현대 웹 개발에서 반드시 알아야 할 핵심 문법들을 정리했습니다.

> 💡 ES6는 JavaScript의 큰 전환점입니다. 화살표 함수, 클래스, 모듈 등의 기능이 추가되었습니다.

## 화살표 함수 (Arrow Function)

기존 함수 표현식보다 짧고 간결하게 작성할 수 있습니다.

```js
// 기존 방식
const add = function(a, b) {
  return a + b;
};

// 화살표 함수
const add = (a, b) => a + b;

// 콜백에서 유용하게 사용
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);
console.log(doubled); // [2, 4, 6, 8, 10]
```

## 비구조화 할당 (Destructuring)

객체나 배열에서 값을 쉽게 추출할 수 있습니다.

```js
// 객체 비구조화
const person = { name: '홍길동', age: 30, city: '서울' };
const { name, age } = person;
console.log(name, age); // '홍길동' 30

// 배열 비구조화
const colors = ['red', 'green', 'blue'];
const [first, , third] = colors;
console.log(first, third); // 'red' 'blue'

// 기본값 설정
const { country = '한국' } = person;
console.log(country); // '한국'
```

## 템플릿 리터럴 (Template Literals)

백틱(`` ` ``)을 사용해 문자열을 더 쉽게 작성합니다.

```js
const name = '홍길동';
const age = 30;

// 기존 방식
const msg1 = '안녕하세요! 저는 ' + name + '이고 ' + age + '살입니다.';

// 템플릿 리터럴
const msg2 = `안녕하세요! 저는 ${name}이고 ${age}살입니다.`;
console.log(msg2);
```

## 주요 문법 비교

| 문법 | ES5 | ES6+ |
|------|-----|------|
| 함수 선언 | `function() {}` | `() => {}` |
| 변수 선언 | `var` | `let`, `const` |
| 문자열 연결 | `'Hello' + name` | `` `Hello ${name}` `` |
| 객체 메서드 | `obj.method = function()` | `obj.method()` |

## 정리

모던 JavaScript는 **가독성**과 **생산성**을 크게 향상시켜 줍니다.
특히 `const`, `let`, 화살표 함수, 비구조화 할당은 매일 사용하게 됩니다.
