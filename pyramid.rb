#!/usr/bin/env ruby
# -*- coding: utf-8 -*-

################################################################################
# defualt
################################################################################
@@n = 4
@@debug = false

################################################################################
# Arguments
################################################################################
require "optparse"
OptionParser.new { |opts|
  # options
  opts.on("-h","--help","Show this message") {
    puts opts
    exit
  }
  opts.on("-n [INPUT]"){ |f|
    @@n = f.to_i
  }
  opts.on("-d", "--debug"){
    @@debug = true
  }
  # parse
  opts.parse!(ARGV)
}

#### size ####
@@size = @@n * (@@n+1) / 2

################################################################################
# Array
################################################################################
class Array
  #### sum ####
  def sum
    self.inject(:+)
  end
  #### combination ####
  def combination(n)
    return [[]]              if n == 0
    return self.map{|i| [i]} if n == 1

    cs = []
    self.combination(n-1).each do |c|
      i = self.index(c.last)
      self[i+1..-1].each do |e|
        cs.push(c + [e])
      end
    end
    cs
  end
  #### permutation ####
  def permutation(n)
    return [[]]              if n == 0
    return self.map{|i| [i]} if n == 1

    ps = []
    self.permutation(n-1).each do |p|
      (self-p).each do |e|
        ps.push(p + [e])
      end
    end
    ps
  end
end

################################################################################
# main
################################################################################
#### depth ####
def depth(index)
  for n in 0..@@n
    i = n * (n+1) / 2
    return n if index < i
  end
  return -1
end

#### sibling ####
# 0: 0
# 1: 1  2
# 2: 3  4  5
# 3: 6  7  8  9
# 4: 10 11 ...
# n: ↑ has no sibling
def has_sibling?(index)
  for n in 0..@@n
    i = n * (n+1) / 2
    return false if index == i
  end
  return true
end
def sibling(index)
  nil if !has_sibling?(index)
  index - 1
end

#### parent ####
# 0:       0
# 1:     1 2
# 2:   3 4 5
# 3: 6 7 8 9
def parent(index)
  return nil if !has_sibling?(index)
  d = depth(index)
  index - d
end

#### e is addable to ary ####
def addable?(ary, e)
  puts "addable?(#{ary}, #{e})" if @@debug

  i = ary.size
  return true if !has_sibling?(i)
  return true if ary[parent(i)] == (ary[sibling(i)] - e).abs
  false
end

#### show solution ####
def show(ary)
  puts "===="
  for n in 0..@@n-1
    s = n * (n+1) / 2
    t = s + n
    puts "#{ary[s..t]}"
  end
end

#### enumerate ####
def enumerate
  nums = Array.new(@@size){|i| i+1}
  cs = [ [] ]
  while cs.size > 0
    c = cs.shift
    p c if @@debug
    #### c is a solution ####
    if c.size == @@size
      show(c)
      next
    end

    #### expand ####
    (nums - c).each do |e|
      cs.push(c + [e]) if addable?(c, e)
    end
  end
end

################################################################################
# main
################################################################################
enumerate
