import React, { useState, useEffect, useRef } from 'react';
import { Star, ChevronLeft, ChevronRight, Quote } from 'lucide-react';
import { mockTestimonials } from '../mock/mockData';

const TestimonialsSection = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isAutoPlaying, setIsAutoPlaying] = useState(true);
  const sectionRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
          }
        });
      },
      { threshold: 0.1 }
    );

    const elements = sectionRef.current?.querySelectorAll('.fade-in-up, .slide-in-left, .slide-in-right, .scale-in');
    elements?.forEach((el) => observer.observe(el));

    return () => observer.disconnect();
  }, []);

  // Auto-play functionality
  useEffect(() => {
    if (!isAutoPlaying) return;

    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % mockTestimonials.length);
    }, 5000);

    return () => clearInterval(interval);
  }, [isAutoPlaying]);

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % mockTestimonials.length);
    setIsAutoPlaying(false);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + mockTestimonials.length) % mockTestimonials.length);
    setIsAutoPlaying(false);
  };

  const goToSlide = (index) => {
    setCurrentSlide(index);
    setIsAutoPlaying(false);
  };

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, index) => (
      <Star
        key={index}
        className={`w-5 h-5 ${
          index < rating
            ? 'text-yellow-400 fill-current'
            : 'text-gray-300'
        }`}
      />
    ));
  };

  return (
    <section id="testimonials" className="py-16 bg-gradient-to-br from-gray-50 to-white" ref={sectionRef}>
      <div className="container">
        <div className="text-center mb-12">
          <h2 className="heading-2 fade-in-up mb-4">
            O Que Dizem os <span style={{color: 'var(--accent-text)'}}>Nossos Traders</span>
          </h2>
          <p className="body-large fade-in-up max-w-2xl mx-auto" style={{animationDelay: '0.2s'}}>
            Histórias reais de sucesso dos traders que confiam na nossa plataforma
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          {/* Main Testimonial Slider */}
          <div className="relative bg-white rounded-3xl shadow-xl p-8 md:p-12 fade-in-up" style={{animationDelay: '0.4s'}}>
            <div
              className="overflow-hidden"
              onMouseEnter={() => setIsAutoPlaying(false)}
              onMouseLeave={() => setIsAutoPlaying(true)}
            >
              <div
                className="flex transition-transform duration-500 ease-in-out"
                style={{ transform: `translateX(-${currentSlide * 100}%)` }}
              >
                {mockTestimonials.map((testimonial, index) => (
                  <div key={testimonial.id} className="w-full flex-shrink-0">
                    <div className="text-center">
                      {/* Quote Icon */}
                      <div className="w-16 h-16 bg-gradient-to-br from-green-100 to-green-200 rounded-full flex items-center justify-center mx-auto mb-6">
                        <Quote className="w-8 h-8" style={{color: 'var(--accent-text)'}} />
                      </div>

                      {/* Rating */}
                      <div className="flex justify-center mb-6">
                        {renderStars(testimonial.rating)}
                      </div>

                      {/* Testimonial Text */}
                      <blockquote className="text-xl md:text-2xl leading-relaxed mb-8 text-gray-700 italic">
                        "{testimonial.text}"
                      </blockquote>

                      {/* Author Info */}
                      <div className="flex items-center justify-center gap-4">
                        {/* Avatar */}
                        <div className="w-16 h-16 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
                          {testimonial.avatar}
                        </div>
                        
                        <div className="text-left">
                          <div className="font-semibold text-lg" style={{color: 'var(--text-primary)'}}>
                            {testimonial.name}
                          </div>
                          <div className="text-sm text-gray-600">{testimonial.role}</div>
                          <div className="text-xs text-gray-500">{testimonial.location}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Navigation Arrows */}
            <button
              onClick={prevSlide}
              className="absolute left-4 top-1/2 transform -translate-y-1/2 w-12 h-12 bg-white shadow-lg rounded-full flex items-center justify-center text-gray-600 hover:text-gray-900 transition-colors duration-200 hover:shadow-xl"
            >
              <ChevronLeft className="w-6 h-6" />
            </button>
            
            <button
              onClick={nextSlide}
              className="absolute right-4 top-1/2 transform -translate-y-1/2 w-12 h-12 bg-white shadow-lg rounded-full flex items-center justify-center text-gray-600 hover:text-gray-900 transition-colors duration-200 hover:shadow-xl"
            >
              <ChevronRight className="w-6 h-6" />
            </button>
          </div>

          {/* Slide Indicators */}
          <div className="flex justify-center mt-8 gap-2">
            {mockTestimonials.map((_, index) => (
              <button
                key={index}
                onClick={() => goToSlide(index)}
                className={`w-3 h-3 rounded-full transition-all duration-300 ${
                  index === currentSlide
                    ? 'w-8 scale-110'
                    : 'hover:scale-110'
                }`}
                style={{
                  backgroundColor: index === currentSlide ? 'var(--accent-primary)' : '#e5e7eb'
                }}
              />
            ))}
          </div>

          {/* Auto-play indicator */}
          <div className="text-center mt-4">
            <button
              onClick={() => setIsAutoPlaying(!isAutoPlaying)}
              className="text-sm text-gray-500 hover:text-gray-700 transition-colors duration-200"
            >
              {isAutoPlaying ? 'Pausar' : 'Reproduzir'} apresentação automática
            </button>
          </div>
        </div>

        {/* Mini testimonials grid */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 fade-in-up" style={{animationDelay: '0.8s'}}>
          {mockTestimonials.map((testimonial, index) => (
            <div
              key={`mini-${testimonial.id}`}
              className={`bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-300 scale-in`}
              style={{animationDelay: `${0.9 + index * 0.1}s`}}
            >
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
                  {testimonial.avatar}
                </div>
                <div>
                  <div className="font-medium text-sm" style={{color: 'var(--text-primary)'}}>
                    {testimonial.name}
                  </div>
                  <div className="flex">
                    {renderStars(testimonial.rating)}
                  </div>
                </div>
              </div>
              <p className="text-sm text-gray-600 italic line-clamp-3">
                "{testimonial.text.length > 100 
                  ? testimonial.text.substring(0, 100) + '...' 
                  : testimonial.text}"
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;