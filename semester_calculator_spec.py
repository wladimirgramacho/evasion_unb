from expects import expect, equal
from mamba import description, context, it

import semester_calculator as SC

with description('calculates semester of course') as self:
  with context('when student starts in first semester of year'):
    with it('when course was taken on first semester'):
      expect(SC.calculate(20001, 20001)).to(equal(1))

    with it('when course was taken on second semester'):
      expect(SC.calculate(20001, 20002)).to(equal(2))

    with it('when course was taken on third semester'):
      expect(SC.calculate(20001, 20011)).to(equal(3))

    with it('when course was taken on fourth semester'):
      expect(SC.calculate(20001, 20012)).to(equal(4))

    with it('when course was taken on summer'):
      expect(SC.calculate(20001, 20010)).to(equal(3))

    with context('started on 20091'):
      with it('when course was taken on first semester'):
        expect(SC.calculate(20091, 20091)).to(equal(1))

      with it('when course was taken on second semester'):
        expect(SC.calculate(20091, 20092)).to(equal(2))

      with it('when course was taken on third semester'):
        expect(SC.calculate(20091, 20101)).to(equal(3))

  with context('when student starts in second semester of year'):
    with it('when course was taken on first semester'):
      expect(SC.calculate(20002, 20002)).to(equal(1))

    with it('when course was taken on second semester'):
      expect(SC.calculate(20002, 20011)).to(equal(2))

    with it('when course was taken on third semester'):
      expect(SC.calculate(20002, 20012)).to(equal(3))

    with it('when course was taken on fourth semester'):
      expect(SC.calculate(20002, 20021)).to(equal(4))

    with it('when course was taken on summer'):
      expect(SC.calculate(20002, 20010)).to(equal(2))

    with context('started on 20092'):
      with it('when course was taken on first semester'):
        expect(SC.calculate(20092, 20092)).to(equal(1))

      with it('when course was taken on second semester'):
        expect(SC.calculate(20092, 20101)).to(equal(2))

      with it('when course was taken on third semester'):
        expect(SC.calculate(20092, 20102)).to(equal(3))

